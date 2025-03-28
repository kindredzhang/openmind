import type { Plugin } from 'vite';
import * as fs from 'fs';
import * as path from 'path';

interface BuildInfo {
  timestamp: number;
  date: string;
  version: string;
  environment?: string;
  gitCommit?: string;
  buildNumber?: string;
}

export default function myPlugin(options: {
  injectGlobal?: boolean;
  reportFileName?: string;
  enableGitInfo?: boolean;
} = {}): Plugin {
  return {
    name: 'build-info-plugin',
    
    apply: 'build', // This plugin only applies during build
    
    configResolved(config) {
      console.log(`Building for ${config.mode} mode`);
    },
    
    buildStart() {
      console.log('Build started at:', new Date().toLocaleString());
    },
    
    // 注入构建信息到全局变量
    transform(code: string, id: string) {
      // Skip injection if not enabled
      if (options.injectGlobal === false) return null;
      
      // Only inject into main entry files
      if (id.endsWith('main.tsx') || id.endsWith('main.jsx') || id.endsWith('main.ts') || id.endsWith('main.js')) {
        // Get git commit hash if enabled
        let gitCommit = '';
        if (options.enableGitInfo) {
          try {
            // In a real plugin, you would get the git commit hash
            // using child_process.execSync('git rev-parse --short HEAD')
            gitCommit = 'abc123'; // Simulated git commit hash
          } catch (e) {
            console.warn('Failed to get git commit hash:', e);
          }
        }
        
        const buildInfo: BuildInfo = {
          timestamp: Date.now(),
          date: new Date().toISOString(),
          version: process.env.npm_package_version || '0.0.0',
          environment: process.env.NODE_ENV,
          gitCommit: options.enableGitInfo ? gitCommit : undefined,
          buildNumber: process.env.BUILD_NUMBER,
        };
        
        console.log('Injecting build info into:', id);
        
        // Note: TypeScript type definitions should be in a separate .d.ts file
        // but we're keeping it simple for this example
        
        return {
          code: `// Injected build info
window.__BUILD_INFO__ = ${JSON.stringify(buildInfo, null, 2)};
${code}`,
          map: null
        };
      }
      return null;
    },
    
    // 生成构建报告 (Generate build report)
    closeBundle() {
      const buildEndTime = new Date();
      // Create a build report with all the information
      const buildReport = {
        timestamp: buildEndTime.getTime(),
        date: buildEndTime.toISOString(),
        environment: typeof process !== 'undefined' ? process.env.NODE_ENV : 'production',
        nodeVersion: typeof process !== 'undefined' ? process.version : 'unknown',
        viteVersion: '4.x.x', // Hardcoded for simplicity
        buildDuration: 'Calculated at runtime', // We can't track build time without persistent state
        os: {
          platform: typeof process !== 'undefined' ? process.platform : 'unknown',
          arch: typeof process !== 'undefined' ? process.arch : 'unknown',
        },
      };
      
      const reportDir = path.resolve('dist');
      if (!fs.existsSync(reportDir)) {
        fs.mkdirSync(reportDir, { recursive: true });
      }
      
      const reportFileName = options.reportFileName || 'build-report.json';
      const reportPath = path.join(reportDir, reportFileName);
      
      fs.writeFileSync(
        reportPath,
        JSON.stringify(buildReport, null, 2)
      );
      
      // Create a human-readable HTML report
      const htmlReport = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Build Report</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    h1 { color: #333; }
    .card { background: #f5f5f5; border-radius: 4px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .label { font-weight: bold; width: 150px; display: inline-block; }
    .value { color: #0066cc; }
  </style>
</head>
<body>
  <h1>Build Report</h1>
  <div class="card">
    <p><span class="label">Build Date:</span> <span class="value">${new Date(buildReport.date).toLocaleString()}</span></p>
    <p><span class="label">Environment:</span> <span class="value">${buildReport.environment || 'Not specified'}</span></p>
    <p><span class="label">Node Version:</span> <span class="value">${buildReport.nodeVersion}</span></p>
    <p><span class="label">Vite Version:</span> <span class="value">${buildReport.viteVersion}</span></p>
    <p><span class="label">Build Duration:</span> <span class="value">${buildReport.buildDuration}</span></p>
    <p><span class="label">Platform:</span> <span class="value">${buildReport.os.platform} (${buildReport.os.arch})</span></p>
  </div>
  <p><small>Generated by build-info-plugin on ${buildReport.date}</small></p>
</body>
</html>`;
      
      fs.writeFileSync(
        path.join(reportDir, 'build-report.html'),
        htmlReport
      );
      
      console.log('Build completed at:', buildEndTime.toLocaleString());
      console.log('Build reports generated at:');
      console.log(`- JSON: ${reportPath}`);
      console.log(`- HTML: ${path.join(reportDir, 'build-report.html')}`);
    },
    

  };
}
