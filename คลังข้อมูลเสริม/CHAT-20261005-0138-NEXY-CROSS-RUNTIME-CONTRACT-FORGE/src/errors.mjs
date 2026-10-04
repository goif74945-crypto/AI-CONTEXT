export class ContractForgeError extends Error {
  constructor(code, message, path = "$") {
    super(`${code} at ${path}: ${message}`);
    this.name = "ContractForgeError";
    this.code = code;
    this.path = path;
  }
}

export function fail(code, message, path = "$") {
  throw new ContractForgeError(code, message, path);
}
