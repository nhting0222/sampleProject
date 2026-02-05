<template>
  <div class="reports">
    <div class="card">
      <h2>📄 Security Reports</h2>
      <p class="subtitle">Generate comprehensive security reports</p>

      <div class="report-types">
        <div class="report-type-card">
          <h3>📊 Daily Security Summary</h3>
          <p>Overview of all security events and incidents from the past 24 hours</p>
          <button class="btn-generate">Generate Report</button>
        </div>

        <div class="report-type-card">
          <h3>📈 Weekly Threat Analysis</h3>
          <p>Detailed analysis of threat patterns and trends</p>
          <button class="btn-generate">Generate Report</button>
        </div>

        <div class="report-type-card">
          <h3>🎯 Incident Response Report</h3>
          <p>Comprehensive incident timeline and response activities</p>
          <button class="btn-generate">Generate Report</button>
        </div>

        <div class="report-type-card">
          <h3>💻 Asset Security Posture</h3>
          <p>Current security status of all monitored assets</p>
          <button class="btn-generate">Generate Report</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reports {
  padding: 2rem;
  min-height: 100%;
  width: 100%;
  background: #f9fafb;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.subtitle {
  color: #6b7280;
  margin-bottom: 2rem;
}

.report-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.report-type-card {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
  transition: border-color 0.3s;
}

.report-type-card:hover {
  border-color: #2563eb;
}

.report-type-card h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.report-type-card p {
  color: #6b7280;
  margin-bottom: 1rem;
}

.btn-generate {
  width: 100%;
  padding: 0.75rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-generate:hover {
  background: #1d4ed8;
}
</style>
