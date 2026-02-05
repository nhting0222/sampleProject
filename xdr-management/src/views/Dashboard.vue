<template>
  <div class="dashboard">
    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card critical">
        <div class="stat-icon">🚨</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.criticalEvents }}</div>
          <div class="stat-label">Critical Events</div>
          <div class="stat-trend up">↑ 12% vs yesterday</div>
        </div>
      </div>

      <div class="stat-card warning">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.activeIncidents }}</div>
          <div class="stat-label">Active Incidents</div>
          <div class="stat-trend down">↓ 8% vs yesterday</div>
        </div>
      </div>

      <div class="stat-card success">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.resolvedToday }}</div>
          <div class="stat-label">Resolved Today</div>
          <div class="stat-trend up">↑ 23% vs yesterday</div>
        </div>
      </div>

      <div class="stat-card info">
        <div class="stat-icon">💻</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.assetsMonitored }}</div>
          <div class="stat-label">Assets Monitored</div>
          <div class="stat-trend neutral">→ No change</div>
        </div>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
      <!-- Event Trend Chart -->
      <div class="card chart-card large">
        <div class="card-header">
          <h3>📈 Event Trends (24 Hours)</h3>
          <div class="header-actions">
            <select v-model="trendTimeRange" class="time-select">
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
            </select>
          </div>
        </div>
        <div class="chart-container">
          <v-chart :option="eventTrendOption" autoresize />
        </div>
      </div>

      <!-- Severity Distribution -->
      <div class="card chart-card">
        <div class="card-header">
          <h3>🎯 Severity Distribution</h3>
        </div>
        <div class="chart-container">
          <v-chart :option="severityPieOption" autoresize />
        </div>
      </div>

      <!-- Event Types -->
      <div class="card chart-card">
        <div class="card-header">
          <h3>📊 Event Types</h3>
        </div>
        <div class="chart-container">
          <v-chart :option="eventTypesOption" autoresize />
        </div>
      </div>

      <!-- Geographic Distribution -->
      <div class="card chart-card large">
        <div class="card-header">
          <h3>🗺️ Geographic Threat Distribution</h3>
          <router-link to="/threat-map" class="view-all">View Full Map →</router-link>
        </div>
        <div class="geo-overview">
          <div
            v-for="location in geoLocations"
            :key="location.name"
            class="geo-item"
            :class="getThreatLevel(location.threats)"
          >
            <div class="geo-icon">📍</div>
            <div class="geo-info">
              <div class="geo-name">{{ location.name }}</div>
              <div class="geo-stats">
                <span class="geo-events">{{ location.events }} events</span>
                <span class="geo-threats" :class="getThreatLevel(location.threats)">
                  {{ location.threats }} threats
                </span>
              </div>
            </div>
            <div class="geo-pulse" v-if="location.threats >= 50"></div>
          </div>
        </div>
      </div>

      <!-- Response Time Trend -->
      <div class="card chart-card">
        <div class="card-header">
          <h3>⏱️ Response Time Trend</h3>
        </div>
        <div class="chart-container">
          <v-chart :option="responseTimeOption" autoresize />
        </div>
      </div>

      <!-- Top Affected Assets -->
      <div class="card chart-card">
        <div class="card-header">
          <h3>💻 Top Affected Assets</h3>
        </div>
        <div class="chart-container">
          <v-chart :option="affectedAssetsOption" autoresize />
        </div>
      </div>

      <!-- Recent Incidents Timeline -->
      <div class="card timeline-card large">
        <div class="card-header">
          <h3>📋 Recent Incidents Timeline</h3>
          <router-link to="/incidents" class="view-all">View All →</router-link>
        </div>
        <div class="timeline-container">
          <div
            v-for="(incident, index) in activeIncidents.slice(0, 8)"
            :key="incident.id"
            class="timeline-item"
            @click="viewIncident(incident.id)"
          >
            <div class="timeline-marker" :class="incident.severity">
              <span class="marker-dot"></span>
              <div v-if="index < activeIncidents.slice(0, 8).length - 1" class="timeline-line"></div>
            </div>
            <div class="timeline-content">
              <div class="timeline-header">
                <span class="timeline-title">{{ incident.title }}</span>
                <span class="timeline-time">{{ formatTime(incident.createdAt) }}</span>
              </div>
              <div class="timeline-meta">
                <span class="timeline-id">{{ incident.id }}</span>
                <span class="timeline-status" :class="incident.status">
                  {{ incident.status.replace('_', ' ') }}
                </span>
                <span class="timeline-assignee">{{ incident.assignee }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MITRE ATT&CK Coverage -->
      <div class="card chart-card">
        <div class="card-header">
          <h3>🛡️ MITRE ATT&CK Coverage</h3>
        </div>
        <div class="chart-container">
          <v-chart :option="mitreAttackOption" autoresize />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useXdrStore } from '../stores/xdr'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import {
  CanvasRenderer
} from 'echarts/renderers'
import {
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  EffectScatterChart,
  RadarChart,
  LinesChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent,
  DataZoomComponent
} from 'echarts/components'

dayjs.extend(relativeTime)

// Register ECharts components
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  EffectScatterChart,
  RadarChart,
  LinesChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent,
  DataZoomComponent
])

const router = useRouter()
const xdrStore = useXdrStore()
const trendTimeRange = ref('24h')

const stats = computed(() => xdrStore.stats)
const activeIncidents = computed(() => xdrStore.activeIncidents)

// Load data on mount
onMounted(async () => {
  await xdrStore.initializeData()
})

// Event Trend Chart Data
const eventTrendOption = computed(() => {
  const hours = []
  const critical = []
  const high = []
  const medium = []
  const low = []

  for (let i = 23; i >= 0; i--) {
    hours.push(dayjs().subtract(i, 'hour').format('HH:00'))
    critical.push(Math.floor(Math.random() * 15) + 5)
    high.push(Math.floor(Math.random() * 25) + 10)
    medium.push(Math.floor(Math.random() * 35) + 15)
    low.push(Math.floor(Math.random() * 20) + 5)
  }

  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: { color: '#1f2937' }
    },
    legend: {
      data: ['Critical', 'High', 'Medium', 'Low'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: hours,
      axisLabel: { rotate: 45 }
    },
    yAxis: {
      type: 'value',
      name: 'Events'
    },
    series: [
      {
        name: 'Critical',
        type: 'line',
        smooth: true,
        data: critical,
        areaStyle: { opacity: 0.3 },
        itemStyle: { color: '#ef4444' }
      },
      {
        name: 'High',
        type: 'line',
        smooth: true,
        data: high,
        areaStyle: { opacity: 0.3 },
        itemStyle: { color: '#f59e0b' }
      },
      {
        name: 'Medium',
        type: 'line',
        smooth: true,
        data: medium,
        areaStyle: { opacity: 0.3 },
        itemStyle: { color: '#3b82f6' }
      },
      {
        name: 'Low',
        type: 'line',
        smooth: true,
        data: low,
        areaStyle: { opacity: 0.3 },
        itemStyle: { color: '#10b981' }
      }
    ]
  }
})

// Severity Distribution Pie Chart
const severityPieOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: 145, name: 'Critical', itemStyle: { color: '#ef4444' } },
        { value: 234, name: 'High', itemStyle: { color: '#f59e0b' } },
        { value: 312, name: 'Medium', itemStyle: { color: '#3b82f6' } },
        { value: 189, name: 'Low', itemStyle: { color: '#10b981' } }
      ]
    }
  ]
}))

// Event Types Bar Chart
const eventTypesOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'value'
  },
  yAxis: {
    type: 'category',
    data: ['Malware', 'Phishing', 'Port Scan', 'Brute Force', 'Data Exfil', 'Suspicious Login']
  },
  series: [
    {
      type: 'bar',
      data: [
        { value: 234, itemStyle: { color: '#ef4444' } },
        { value: 189, itemStyle: { color: '#f59e0b' } },
        { value: 167, itemStyle: { color: '#f59e0b' } },
        { value: 145, itemStyle: { color: '#3b82f6' } },
        { value: 98, itemStyle: { color: '#ef4444' } },
        { value: 87, itemStyle: { color: '#10b981' } }
      ],
      barWidth: '60%',
      itemStyle: { borderRadius: [0, 5, 5, 0] }
    }
  ]
}))

// Geographic Locations Data
const geoLocations = ref([
  { name: 'Seoul HQ', events: 234, threats: 89 },
  { name: 'Busan Office', events: 156, threats: 67 },
  { name: 'Incheon DC', events: 145, threats: 54 },
  { name: 'Daegu Branch', events: 98, threats: 43 },
  { name: 'Daejeon R&D', events: 87, threats: 32 },
  { name: 'Gwangju Office', events: 76, threats: 28 }
])

const getThreatLevel = (threats) => {
  if (threats >= 80) return 'critical'
  if (threats >= 50) return 'high'
  if (threats >= 20) return 'medium'
  return 'low'
}

// Response Time Chart
const responseTimeOption = computed(() => {
  const days = []
  const responseTime = []

  for (let i = 6; i >= 0; i--) {
    days.push(dayjs().subtract(i, 'day').format('MM/DD'))
    responseTime.push((Math.random() * 20 + 15).toFixed(1))
  }

  return {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>Avg: {c} min'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: days
    },
    yAxis: {
      type: 'value',
      name: 'Minutes'
    },
    series: [
      {
        type: 'line',
        smooth: true,
        data: responseTime,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0)' }
            ]
          }
        },
        itemStyle: { color: '#3b82f6' },
        lineStyle: { width: 3 }
      }
    ]
  }
})

// Affected Assets
const affectedAssetsOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    max: 100
  },
  yAxis: {
    type: 'category',
    data: ['WS-101', 'SRV-WEB-01', 'SRV-DB-01', 'LAPTOP-HR-05', 'WS-205']
  },
  series: [
    {
      type: 'bar',
      data: [
        { value: 92, itemStyle: { color: '#ef4444' } },
        { value: 85, itemStyle: { color: '#ef4444' } },
        { value: 73, itemStyle: { color: '#f59e0b' } },
        { value: 68, itemStyle: { color: '#f59e0b' } },
        { value: 54, itemStyle: { color: '#3b82f6' } }
      ],
      barWidth: '50%',
      itemStyle: { borderRadius: [0, 5, 5, 0] },
      label: {
        show: true,
        position: 'right',
        formatter: '{c}%'
      }
    }
  ]
}))

// MITRE ATT&CK Radar
const mitreAttackOption = computed(() => ({
  tooltip: {
    trigger: 'item'
  },
  radar: {
    indicator: [
      { name: 'Initial Access', max: 100 },
      { name: 'Execution', max: 100 },
      { name: 'Persistence', max: 100 },
      { name: 'Privilege Esc.', max: 100 },
      { name: 'Defense Evasion', max: 100 },
      { name: 'Lateral Movement', max: 100 }
    ],
    shape: 'circle',
    splitNumber: 4,
    axisName: {
      color: '#6b7280'
    },
    splitLine: {
      lineStyle: { color: '#e5e7eb' }
    },
    splitArea: {
      show: true,
      areaStyle: {
        color: ['rgba(59, 130, 246, 0.05)', 'rgba(59, 130, 246, 0.1)']
      }
    }
  },
  series: [
    {
      type: 'radar',
      data: [
        {
          value: [85, 72, 68, 91, 79, 64],
          name: 'Detection Coverage',
          areaStyle: {
            color: 'rgba(59, 130, 246, 0.3)'
          },
          itemStyle: {
            color: '#3b82f6'
          }
        }
      ]
    }
  ]
}))

const formatTime = (timestamp) => {
  return dayjs(timestamp).fromNow()
}

const viewIncident = (id) => {
  router.push(`/incidents/${id}`)
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  background: #f9fafb;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-left: 4px solid;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.critical {
  border-left-color: #ef4444;
}

.stat-card.warning {
  border-left-color: #f59e0b;
}

.stat-card.success {
  border-left-color: #10b981;
}

.stat-card.info {
  border-left-color: #3b82f6;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.stat-trend {
  font-size: 0.8rem;
  font-weight: 500;
  margin-top: 0.5rem;
  opacity: 0.8;
}

.stat-card.critical .stat-trend.up {
  color: #ef4444;
}

.stat-card.warning .stat-trend.down {
  color: #10b981;
}

.stat-card.success .stat-trend.up {
  color: #10b981;
}

.stat-card.info .stat-trend.neutral {
  color: #6b7280;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chart-card.large {
  grid-column: span 2;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1f2937;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.time-select {
  padding: 0.4rem 0.8rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.85rem;
  background: white;
  cursor: pointer;
}

.view-all {
  color: #2563eb;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
}

.view-all:hover {
  text-decoration: underline;
}

.map-legend {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.map-legend .legend-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: #6b7280;
}

.map-legend .legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.map-legend .legend-dot.critical {
  background: #ef4444;
}

.map-legend .legend-dot.high {
  background: #f59e0b;
}

.map-legend .legend-dot.medium {
  background: #3b82f6;
}

.map-legend .legend-dot.low {
  background: #10b981;
}

.geo-overview {
  padding: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.geo-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: #f9fafb;
  border-radius: 10px;
  border-left: 4px solid;
  position: relative;
  transition: all 0.3s ease;
  cursor: pointer;
}

.geo-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.geo-item.critical {
  border-left-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
}

.geo-item.high {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}

.geo-item.medium {
  border-left-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.geo-item.low {
  border-left-color: #10b981;
  background: linear-gradient(135deg, #f0fdf4 0%, #d1fae5 100%);
}

.geo-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.geo-info {
  flex: 1;
  min-width: 0;
}

.geo-name {
  font-weight: 700;
  font-size: 1rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.geo-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
}

.geo-events {
  color: #6b7280;
}

.geo-threats {
  font-weight: 600;
}

.geo-threats.critical {
  color: #dc2626;
}

.geo-threats.high {
  color: #d97706;
}

.geo-threats.medium {
  color: #2563eb;
}

.geo-threats.low {
  color: #059669;
}

.geo-pulse {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
}

.chart-container {
  padding: 1rem;
  flex: 1;
  min-height: 350px;
  height: 100%;
}

.chart-card.large .chart-container {
  min-height: 400px;
}

.timeline-container {
  padding: 1rem 1.5rem;
  max-height: 500px;
  overflow-y: auto;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: background 0.2s;
  padding: 0.5rem;
  border-radius: 8px;
}

.timeline-item:hover {
  background: #f9fafb;
}

.timeline-marker {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.marker-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 3px solid;
  background: white;
  z-index: 1;
}

.timeline-marker.critical .marker-dot {
  border-color: #ef4444;
}

.timeline-marker.high .marker-dot {
  border-color: #f59e0b;
}

.timeline-marker.medium .marker-dot {
  border-color: #3b82f6;
}

.timeline-line {
  width: 2px;
  flex: 1;
  background: #e5e7eb;
  margin-top: 0.5rem;
}

.timeline-content {
  flex: 1;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.timeline-title {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.95rem;
}

.timeline-time {
  font-size: 0.8rem;
  color: #9ca3af;
}

.timeline-meta {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  font-size: 0.85rem;
}

.timeline-id {
  color: #2563eb;
  font-family: monospace;
  font-weight: 500;
}

.timeline-status {
  padding: 0.2rem 0.6rem;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.timeline-status.in_progress {
  background: #fef3c7;
  color: #92400e;
}

.timeline-status.resolved {
  background: #d1fae5;
  color: #065f46;
}

.timeline-assignee {
  color: #6b7280;
}

/* Tablet */
@media (max-width: 1024px) {
  .dashboard {
    padding: 1.5rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .chart-card.large {
    grid-column: span 1;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .geo-overview {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile */
@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-icon {
    font-size: 2rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .charts-grid {
    gap: 1rem;
  }

  .card-header {
    padding: 1rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .card-header h3 {
    font-size: 1rem;
  }

  .header-actions {
    width: 100%;
  }

  .time-select {
    width: 100%;
  }

  .chart-container {
    min-height: 250px;
    padding: 0.5rem;
  }

  .chart-card.large .chart-container {
    min-height: 300px;
  }

  .geo-overview {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .geo-item {
    padding: 1rem;
  }

  .timeline-container {
    padding: 1rem;
  }

  .timeline-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .timeline-marker {
    display: none;
  }

  .map-legend {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .map-legend .legend-item {
    font-size: 0.8rem;
  }
}

</style>
