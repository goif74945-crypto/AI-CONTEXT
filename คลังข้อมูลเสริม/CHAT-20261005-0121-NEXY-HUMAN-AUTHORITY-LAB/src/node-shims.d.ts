declare module "node:crypto" {
  export interface Hash {
    update(data: string, inputEncoding?: string): Hash;
    digest(encoding: "hex"): string;
  }
  export function createHash(algorithm: string): Hash;
}

declare module "node:fs/promises" {
  export function readFile(path: string, encoding: "utf8"): Promise<string>;
}

declare const process: {
  argv: string[];
  stdout: { write(value: string): void };
  stderr: { write(value: string): void };
  exitCode?: number;
};
