import { generateKeyPairSync } from 'crypto';
import fetch from 'node-fetch';

export async function generateNodeKeys(nodeId: string) {
  const { publicKey, privateKey } = generateKeyPairSync('rsa', {
    modulusLength: 4096,
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem'
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem'
    }
  });
  
  return { publicKey, privateKey };
}

export async function registerNode(
  centralUrl: string,
  token: string,
  nodeInfo: any
) {
  const response = await fetch(`${centralUrl}/api/nodes/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(nodeInfo),
  });
  
  if (!response.ok) {
    throw new Error(`Registration failed: ${response.statusText}`);
  }
  
  return await response.json();
}
