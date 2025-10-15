import { describe, it, expect } from 'vitest';

describe('Example Unit Test', () => {
  it('should pass basic assertion', () => {
    expect(1 + 1).toBe(2);
  });
  
  it('should test async code', async () => {
    const result = await Promise.resolve(42);
    expect(result).toBe(42);
  });
});
