const NODE_ID = process.env.NODE_ID || 'unknown';
const CENTRAL_URL = process.env.CENTRAL_URL || 'http://localhost:3000';

async function collectMetrics() {
  const metrics = {
    nodeId: NODE_ID,
    timestamp: new Date().toISOString(),
    cpu: process.cpuUsage(),
    memory: process.memoryUsage(),
    uptime: process.uptime()
  };
  
  console.log('Collected metrics:', metrics);
  
  try {
    // Would send to central server
    // await fetch(`${CENTRAL_URL}/telemetry/report`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(metrics)
    // });
    console.log('Metrics reported (simulated)');
  } catch (error) {
    console.error('Failed to report metrics:', error);
  }
}

// Collect metrics every 60 seconds
setInterval(collectMetrics, 60000);

// Initial collection
collectMetrics();

console.log(`🔍 Telemetry agent started for node: ${NODE_ID}`);
