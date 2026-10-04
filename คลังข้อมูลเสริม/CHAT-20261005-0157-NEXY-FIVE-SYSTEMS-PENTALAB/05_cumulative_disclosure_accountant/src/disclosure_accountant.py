from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable


class DisclosureInputError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class DisclosureItem:
    item_id: str
    category: str
    points: int
    linkability_group: str


@dataclass(frozen=True, slots=True)
class DisclosureEvent:
    event_id: str
    audience: str
    purpose: str
    item_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DisclosurePolicy:
    max_audience_points: int
    max_category_points: tuple[tuple[str, int], ...] = ()
    review_threshold_bps: int = 8000


@dataclass(frozen=True, slots=True)
class LedgerState:
    audience_items: tuple[tuple[str, tuple[str, ...]], ...] = ()
    accepted_events: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DisclosureDecision:
    status: str
    projected_audience_points: int
    projected_category_points: tuple[tuple[str, int], ...]
    newly_disclosed_items: tuple[str, ...]
    reason_codes: tuple[str, ...]
    receipt_hash: str
    next_state: LedgerState


def _clean(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise DisclosureInputError(f"{field}:NOT_STRING")
    value=value.strip()
    if not value:
        raise DisclosureInputError(f"{field}:EMPTY")
    return value


def _normalize_items(items: Iterable[DisclosureItem]) -> dict[str, DisclosureItem]:
    result={}
    for item in items:
        iid=_clean(item.item_id,"item_id")
        if iid in result: raise DisclosureInputError(f"DUPLICATE_ITEM:{iid}")
        category=_clean(item.category,f"{iid}.category")
        group=_clean(item.linkability_group,f"{iid}.linkability_group")
        if not isinstance(item.points,int) or item.points<0: raise DisclosureInputError(f"{iid}:INVALID_POINTS")
        result[iid]=DisclosureItem(iid,category,item.points,group)
    return result


def _normalize_policy(policy: DisclosurePolicy) -> dict[str,int]:
    if not isinstance(policy.max_audience_points,int) or policy.max_audience_points<0: raise DisclosureInputError("INVALID_AUDIENCE_BUDGET")
    if not isinstance(policy.review_threshold_bps,int) or not 0<=policy.review_threshold_bps<=10_000: raise DisclosureInputError("INVALID_REVIEW_THRESHOLD")
    cats={}
    for category,budget in policy.max_category_points:
        category=_clean(category,"policy.category")
        if category in cats: raise DisclosureInputError(f"DUPLICATE_CATEGORY_BUDGET:{category}")
        if not isinstance(budget,int) or budget<0: raise DisclosureInputError(f"INVALID_CATEGORY_BUDGET:{category}")
        cats[category]=budget
    return cats


def _state_map(state: LedgerState) -> dict[str,set[str]]:
    result={}
    for audience,item_ids in state.audience_items:
        audience=_clean(audience,"state.audience")
        if audience in result: raise DisclosureInputError(f"DUPLICATE_STATE_AUDIENCE:{audience}")
        result[audience]={_clean(i,f"state.{audience}.item") for i in item_ids}
    if len(state.accepted_events)!=len(set(state.accepted_events)): raise DisclosureInputError("DUPLICATE_ACCEPTED_EVENT")
    return result


def evaluate_disclosure(catalog: Iterable[DisclosureItem], state: LedgerState, event: DisclosureEvent, policy: DisclosurePolicy) -> DisclosureDecision:
    items=_normalize_items(catalog); category_budgets=_normalize_policy(policy); state_map=_state_map(state)
    event_id=_clean(event.event_id,"event_id"); audience=_clean(event.audience,"audience"); purpose=_clean(event.purpose,"purpose")
    requested=tuple(sorted({_clean(i,"event.item_id") for i in event.item_ids}))
    if not requested: raise DisclosureInputError("EMPTY_DISCLOSURE_EVENT")
    unknown=sorted(set(requested)-items.keys())
    if unknown: raise DisclosureInputError(f"UNKNOWN_ITEM:{unknown}")
    if event_id in state.accepted_events: raise DisclosureInputError(f"EVENT_ID_REPLAY:{event_id}")

    already=state_map.get(audience,set()); new_ids=tuple(sorted(set(requested)-already)); projected_ids=already|set(requested)
    projected_total=sum(items[i].points for i in projected_ids); category_totals={}; group_totals={}
    for iid in projected_ids:
        item=items[iid]
        category_totals[item.category]=category_totals.get(item.category,0)+item.points
        group_totals[item.linkability_group]=group_totals.get(item.linkability_group,0)+item.points
    reasons=set()
    if projected_total>policy.max_audience_points: reasons.add("AUDIENCE_CUMULATIVE_BUDGET_EXCEEDED")
    for category,budget in category_budgets.items():
        if category_totals.get(category,0)>budget: reasons.add(f"CATEGORY_BUDGET_EXCEEDED:{category}")
    if policy.max_audience_points>0:
        half=policy.max_audience_points//2
        for group,points in group_totals.items():
            if points>half: reasons.add(f"LINKABILITY_CONCENTRATION:{group}")

    if reasons:
        status="FREEZE"; next_state=state
    else:
        threshold=(policy.max_audience_points*policy.review_threshold_bps)//10_000
        status="REVIEW" if projected_total>=threshold and policy.max_audience_points>0 else "ALLOW"
        if status=="REVIEW":
            reasons.add("CUMULATIVE_BUDGET_NEAR_LIMIT"); next_state=state
        else:
            updated=dict(state_map); updated[audience]=set(projected_ids)
            next_state=LedgerState(tuple(sorted((a,tuple(sorted(ids))) for a,ids in updated.items())),tuple(sorted((*state.accepted_events,event_id))))

    payload={"event":{"event_id":event_id,"audience":audience,"purpose":purpose,"item_ids":requested},"status":status,"projected_audience_points":projected_total,"projected_category_points":dict(sorted(category_totals.items())),"newly_disclosed_items":new_ids,"reason_codes":sorted(reasons),"policy":{"max_audience_points":policy.max_audience_points,"max_category_points":dict(sorted(category_budgets.items())),"review_threshold_bps":policy.review_threshold_bps},"prior_state":{"audience_items":[(a,sorted(ids)) for a,ids in sorted(state_map.items())],"accepted_events":sorted(state.accepted_events)}}
    receipt=sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return DisclosureDecision(status,projected_total,tuple(sorted(category_totals.items())),new_ids,tuple(sorted(reasons)),receipt,next_state)
