declare module 'node:crypto' {
  interface Hash {
    update(data: string, inputEncoding?: string): Hash;
    digest(encoding: 'hex'): string;
  }
  export function createHash(algorithm: string): Hash;
}
