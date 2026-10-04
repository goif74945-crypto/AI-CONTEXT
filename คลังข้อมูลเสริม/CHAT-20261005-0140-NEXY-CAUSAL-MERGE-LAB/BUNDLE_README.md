# Code/Test Bundle Reconstruction

The exact standalone TypeScript source, tests, configs, and local type declaration are stored as four base64 text parts so the GitHub connector can preserve the sandbox-tested bytes losslessly.

Concatenate in numeric order:

```sh
cat CODE_TEST_BUNDLE.b64.part01 \
    CODE_TEST_BUNDLE.b64.part02 \
    CODE_TEST_BUNDLE.b64.part03 \
    CODE_TEST_BUNDLE.b64.part04 \
  | base64 -d > CODE_TEST_BUNDLE.tar.gz
```

Verify:

```text
SHA-256 7f2e8d086f729597b0427ca7ea20949c7df7803a1745517644d8b89fafdea4ab
```

Extract:

```sh
tar -xzf CODE_TEST_BUNDLE.tar.gz
npm run verify
```

Part SHA-256:
- part01 ebc88b1c8dbc310731d895221db47365e8e19543f225df0afd12954c71676d22
- part02 e39322a184ab90f96bceaae22e1027878f7bd4c3e7acfecbf0b3fdf8531a4f91
- part03 c131567a855b8ad0d7aeaf820e00d87f29beeb52918351373e39fa8cce3166b1
- part04 4261a498fc1370b610c6d692782b91aae9771532ba0f87d30ec6fc0f0728159a

This bundle is experimental supplemental work. It imports no protected NEXY.AI repository code and is not proof of live NEXY integration.
