<template>
  <div class="threat-map">
    <div class="map-header">
      <div class="header-left">
        <h1>🗺️ Geographic Threat Map</h1>
        <p class="subtitle">Real-time security threat distribution across South Korea</p>
      </div>
      <div class="header-right">
        <div class="filter-group">
          <label>Time Range:</label>
          <select v-model="timeRange" class="filter-select">
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Threat Level:</label>
          <select v-model="threatFilter" class="filter-select">
            <option value="all">All Levels</option>
            <option value="critical">Critical Only</option>
            <option value="high">High & Above</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Map Legend -->
    <div class="map-legend-section">
      <div class="legend-title">Threat Levels</div>
      <div class="legend-items">
        <div class="legend-item">
          <span class="legend-marker critical"></span>
          <span class="legend-text">Critical (80+)</span>
          <span class="legend-count">{{ criticalCount }}</span>
        </div>
        <div class="legend-item">
          <span class="legend-marker high"></span>
          <span class="legend-text">High (50-79)</span>
          <span class="legend-count">{{ highCount }}</span>
        </div>
        <div class="legend-item">
          <span class="legend-marker medium"></span>
          <span class="legend-text">Medium (20-49)</span>
          <span class="legend-count">{{ mediumCount }}</span>
        </div>
        <div class="legend-item">
          <span class="legend-marker low"></span>
          <span class="legend-text">Low (0-19)</span>
          <span class="legend-count">{{ lowCount }}</span>
        </div>
      </div>
    </div>

    <!-- Main Map Visualization -->
    <div class="map-container">
      <div class="map-chart" ref="mapChartRef">
        <v-chart :option="mapOption" autoresize @click="handleLocationClick" />
      </div>
    </div>

    <!-- Location Details Grid -->
    <div class="locations-grid">
      <div
        v-for="location in filteredLocations"
        :key="location.name"
        class="location-card"
        :class="getThreatLevel(location.threats)"
        @click="selectLocation(location)"
      >
        <div class="card-header">
          <div class="location-name">
            <span class="location-icon">📍</span>
            {{ location.name }}
          </div>
          <div class="threat-badge" :class="getThreatLevel(location.threats)">
            {{ location.threats }}
          </div>
        </div>
        <div class="card-body">
          <div class="stat-row">
            <span class="stat-label">Total Events:</span>
            <span class="stat-value">{{ location.events }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Active Threats:</span>
            <span class="stat-value threat">{{ location.activeThreats }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Incidents:</span>
            <span class="stat-value">{{ location.incidents }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Assets:</span>
            <span class="stat-value">{{ location.assets }}</span>
          </div>
        </div>
        <div class="card-footer">
          <span class="last-update">Updated {{ formatTime(location.lastUpdate) }}</span>
          <button class="details-btn" @click.stop="viewDetails(location)">
            View Details →
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import VChart from 'vue-echarts'
import { use, registerMap } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { MapChart, ScatterChart, EffectScatterChart, LinesChart } from 'echarts/charts'
import { TooltipComponent, GeoComponent, VisualMapComponent } from 'echarts/components'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

use([
  CanvasRenderer,
  MapChart,
  ScatterChart,
  EffectScatterChart,
  LinesChart,
  TooltipComponent,
  GeoComponent,
  VisualMapComponent
])

// South Korea GeoJSON (simplified)
const koreaGeoJson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "South Korea" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [126.0, 38.5], [126.5, 38.3], [127.0, 38.4], [127.5, 38.3],
          [128.0, 38.5], [128.5, 38.3], [129.0, 38.0], [129.3, 37.5],
          [129.5, 37.0], [129.4, 36.5], [129.5, 36.0], [129.4, 35.5],
          [129.2, 35.2], [129.0, 35.1], [128.5, 35.0], [128.0, 35.0],
          [127.5, 34.8], [127.0, 34.6], [126.5, 34.5], [126.3, 34.7],
          [126.1, 35.0], [126.0, 35.5], [125.8, 36.0], [126.0, 36.5],
          [126.2, 37.0], [126.5, 37.5], [126.3, 37.8], [126.0, 38.0],
          [126.0, 38.5]
        ]]
      }
    }
  ]
}

// Register South Korea map
registerMap('SouthKorea', koreaGeoJson)

const router = useRouter()
const timeRange = ref('24h')
const threatFilter = ref('all')
const mapChartRef = ref(null)

// Location data with actual Korean city coordinates (longitude, latitude)
const locations = ref([
  {
    name: 'Seoul HQ',
    coord: [126.9780, 37.5665], // Seoul
    events: 234,
    threats: 89,
    activeThreats: 12,
    incidents: 8,
    assets: 156,
    lastUpdate: new Date(),
    region: 'Seoul',
    ip: '10.0.1.0/24'
  },
  {
    name: 'Busan Office',
    coord: [129.0756, 35.1796], // Busan
    events: 156,
    threats: 67,
    activeThreats: 8,
    incidents: 5,
    assets: 98,
    lastUpdate: new Date(Date.now() - 5 * 60000),
    region: 'Busan',
    ip: '10.0.2.0/24'
  },
  {
    name: 'Incheon DC',
    coord: [126.7052, 37.4563], // Incheon
    events: 145,
    threats: 54,
    activeThreats: 6,
    incidents: 4,
    assets: 87,
    lastUpdate: new Date(Date.now() - 2 * 60000),
    region: 'Incheon',
    ip: '10.0.3.0/24'
  },
  {
    name: 'Daegu Branch',
    coord: [128.6014, 35.8714], // Daegu
    events: 98,
    threats: 43,
    activeThreats: 4,
    incidents: 3,
    assets: 67,
    lastUpdate: new Date(Date.now() - 8 * 60000),
    region: 'Daegu',
    ip: '10.0.4.0/24'
  },
  {
    name: 'Daejeon R&D',
    coord: [127.3845, 36.3504], // Daejeon
    events: 87,
    threats: 32,
    activeThreats: 3,
    incidents: 2,
    assets: 54,
    lastUpdate: new Date(Date.now() - 3 * 60000),
    region: 'Daejeon',
    ip: '10.0.5.0/24'
  },
  {
    name: 'Gwangju Office',
    coord: [126.8526, 35.1595], // Gwangju
    events: 76,
    threats: 28,
    activeThreats: 2,
    incidents: 2,
    assets: 45,
    lastUpdate: new Date(Date.now() - 10 * 60000),
    region: 'Gwangju',
    ip: '10.0.6.0/24'
  },
  {
    name: 'Ulsan Plant',
    coord: [129.3114, 35.5384], // Ulsan
    events: 65,
    threats: 25,
    activeThreats: 2,
    incidents: 1,
    assets: 34,
    lastUpdate: new Date(Date.now() - 6 * 60000),
    region: 'Ulsan',
    ip: '10.0.7.0/24'
  },
  {
    name: 'Suwon Branch',
    coord: [127.0286, 37.2636], // Suwon
    events: 54,
    threats: 18,
    activeThreats: 1,
    incidents: 1,
    assets: 28,
    lastUpdate: new Date(Date.now() - 4 * 60000),
    region: 'Suwon',
    ip: '10.0.8.0/24'
  },
  {
    name: 'Jeju Office',
    coord: [126.5312, 33.4996], // Jeju
    events: 42,
    threats: 15,
    activeThreats: 1,
    incidents: 0,
    assets: 22,
    lastUpdate: new Date(Date.now() - 12 * 60000),
    region: 'Jeju',
    ip: '10.0.9.0/24'
  },
  {
    name: 'Changwon Factory',
    coord: [128.6811, 35.2280], // Changwon
    events: 38,
    threats: 12,
    activeThreats: 1,
    incidents: 0,
    assets: 18,
    lastUpdate: new Date(Date.now() - 15 * 60000),
    region: 'Changwon',
    ip: '10.0.10.0/24'
  }
])

const filteredLocations = computed(() => {
  return locations.value.filter(loc => {
    if (threatFilter.value === 'critical') return loc.threats >= 80
    if (threatFilter.value === 'high') return loc.threats >= 50
    return true
  })
})

const criticalCount = computed(() => locations.value.filter(l => l.threats >= 80).length)
const highCount = computed(() => locations.value.filter(l => l.threats >= 50 && l.threats < 80).length)
const mediumCount = computed(() => locations.value.filter(l => l.threats >= 20 && l.threats < 50).length)
const lowCount = computed(() => locations.value.filter(l => l.threats < 20).length)

const getThreatLevel = (threats) => {
  if (threats >= 80) return 'critical'
  if (threats >= 50) return 'high'
  if (threats >= 20) return 'medium'
  return 'low'
}

const getThreatColor = (threats) => {
  if (threats >= 80) return '#ef4444'
  if (threats >= 50) return '#f59e0b'
  if (threats >= 20) return '#3b82f6'
  return '#10b981'
}

const mapOption = computed(() => ({
  backgroundColor: '#f0f4f8',
  tooltip: {
    trigger: 'item',
    formatter: (params) => {
      if (!params.data || !params.data.name) return ''
      const loc = locations.value.find(l => l.name === params.data.name)
      if (!loc) return params.data.name
      return `<div style="padding: 12px; min-width: 200px;">
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #1f2937;">
          📍 ${loc.name}
        </div>
        <div style="display: grid; gap: 4px;">
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #6b7280;">Events:</span>
            <strong style="color: #1f2937;">${loc.events}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #6b7280;">Threats:</span>
            <strong style="color: ${getThreatColor(loc.threats)};">${loc.threats}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #6b7280;">Active:</span>
            <strong style="color: #ef4444;">${loc.activeThreats}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #6b7280;">Incidents:</span>
            <strong style="color: #1f2937;">${loc.incidents}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #6b7280;">Assets:</span>
            <strong style="color: #1f2937;">${loc.assets}</strong>
          </div>
        </div>
      </div>`
    },
    backgroundColor: 'rgba(255, 255, 255, 0.98)',
    borderColor: '#e5e7eb',
    borderWidth: 1,
    textStyle: { color: '#1f2937' }
  },
  geo: {
    map: 'SouthKorea',
    roam: true,
    zoom: 1.2,
    center: [127.5, 36.0],
    scaleLimit: {
      min: 0.8,
      max: 5
    },
    itemStyle: {
      areaColor: '#e8f4f8',
      borderColor: '#91d5ff',
      borderWidth: 2,
      shadowColor: 'rgba(0, 0, 0, 0.1)',
      shadowBlur: 10
    },
    emphasis: {
      itemStyle: {
        areaColor: '#bae7ff',
        borderColor: '#69c0ff',
        borderWidth: 3
      }
    },
    label: {
      show: false
    }
  },
  series: [
    // Background scatter (all locations)
    {
      name: 'Locations',
      type: 'scatter',
      coordinateSystem: 'geo',
      symbolSize: (val) => {
        const size = val[2] / 3
        return Math.max(size, 20)
      },
      data: filteredLocations.value.map(loc => ({
        name: loc.name,
        value: [...loc.coord, loc.events],
        itemStyle: {
          color: getThreatColor(loc.threats),
          borderColor: '#fff',
          borderWidth: 3,
          shadowColor: getThreatColor(loc.threats),
          shadowBlur: 15
        }
      })),
      label: {
        show: true,
        position: 'top',
        formatter: '{b}',
        fontSize: 11,
        fontWeight: 'bold',
        color: '#1f2937',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        padding: [4, 8],
        borderRadius: 4,
        distance: 10
      },
      emphasis: {
        scale: 1.5
      },
      zlevel: 2
    },
    // Ripple effect for high threat locations
    {
      name: 'High Threat Alert',
      type: 'effectScatter',
      coordinateSystem: 'geo',
      symbolSize: (val) => {
        const size = val[2] / 3
        return Math.max(size, 25)
      },
      data: filteredLocations.value
        .filter(loc => loc.threats >= 50)
        .map(loc => ({
          name: loc.name,
          value: [...loc.coord, loc.events],
          itemStyle: {
            color: getThreatColor(loc.threats)
          }
        })),
      showEffectOn: 'render',
      rippleEffect: {
        brushType: 'stroke',
        scale: 4,
        period: 3
      },
      zlevel: 1
    },
    // Connection lines from Seoul (HQ) to other locations
    {
      name: 'Connections',
      type: 'lines',
      coordinateSystem: 'geo',
      zlevel: 0,
      effect: {
        show: true,
        period: 4,
        trailLength: 0.3,
        symbol: 'arrow',
        symbolSize: 6,
        color: '#3b82f6'
      },
      lineStyle: {
        color: '#93c5fd',
        width: 1,
        curveness: 0.3,
        opacity: 0.6
      },
      data: filteredLocations.value
        .filter(loc => loc.name !== 'Seoul HQ')
        .map(loc => ({
          coords: [
            [126.9780, 37.5665], // Seoul
            loc.coord
          ]
        }))
    }
  ]
}))

const formatTime = (timestamp) => {
  return dayjs(timestamp).fromNow()
}

const handleLocationClick = (params) => {
  if (params.data && params.data.name) {
    const location = locations.value.find(l => l.name === params.data.name)
    if (location) {
      selectLocation(location)
    }
  }
}

const selectLocation = (location) => {
  console.log('Selected location:', location)
}

const viewDetails = (location) => {
  console.log('View details for:', location)
}

onMounted(() => {
  console.log('Threat Map loaded with South Korea map')
})
</script>

<style scoped>
.threat-map {
  padding: 2rem;
  background: #f9fafb;
  min-height: 100%;
  width: 100%;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 2rem;
}

.header-left h1 {
  margin: 0;
  font-size: 2rem;
  color: #1f2937;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  color: #6b7280;
  font-size: 1rem;
}

.header-right {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6b7280;
}

.filter-select {
  padding: 0.6rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  font-size: 0.9rem;
  cursor: pointer;
  min-width: 180px;
}

.map-legend-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.legend-title {
  font-weight: 700;
  font-size: 1rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.legend-items {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.legend-marker {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.legend-marker.critical {
  background: #ef4444;
}

.legend-marker.high {
  background: #f59e0b;
}

.legend-marker.medium {
  background: #3b82f6;
}

.legend-marker.low {
  background: #10b981;
}

.legend-text {
  font-size: 0.9rem;
  color: #6b7280;
}

.legend-count {
  font-weight: 700;
  color: #1f2937;
  background: #f3f4f6;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

.map-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 2rem;
}

.map-chart {
  height: 600px;
  padding: 1rem;
}

.locations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.location-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-left: 4px solid;
  transition: all 0.3s ease;
  cursor: pointer;
}

.location-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.location-card.critical {
  border-left-color: #ef4444;
}

.location-card.high {
  border-left-color: #f59e0b;
}

.location-card.medium {
  border-left-color: #3b82f6;
}

.location-card.low {
  border-left-color: #10b981;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid #f3f4f6;
}

.location-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.location-icon {
  font-size: 1.2rem;
}

.threat-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
}

.threat-badge.critical {
  background: #fee2e2;
  color: #991b1b;
}

.threat-badge.high {
  background: #fef3c7;
  color: #92400e;
}

.threat-badge.medium {
  background: #dbeafe;
  color: #1e40af;
}

.threat-badge.low {
  background: #d1fae5;
  color: #065f46;
}

.card-body {
  padding: 1.25rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f9fafb;
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-label {
  color: #6b7280;
  font-size: 0.9rem;
}

.stat-value {
  font-weight: 700;
  color: #1f2937;
}

.stat-value.threat {
  color: #ef4444;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background: #f9fafb;
  border-top: 1px solid #f3f4f6;
}

.last-update {
  font-size: 0.85rem;
  color: #9ca3af;
}

.details-btn {
  padding: 0.5rem 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.details-btn:hover {
  background: #1d4ed8;
}

/* Tablet */
@media (max-width: 1024px) {
  .threat-map {
    padding: 1.5rem;
  }

  .map-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-right {
    width: 100%;
  }

  .filter-select {
    width: 100%;
  }

  .locations-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile */
@media (max-width: 768px) {
  .threat-map {
    padding: 1rem;
  }

  .header-left h1 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.9rem;
  }

  .filter-group {
    width: 100%;
  }

  .filter-group label {
    font-size: 0.8rem;
  }

  .filter-select {
    min-width: auto;
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
  }

  .map-legend-section {
    padding: 1rem;
  }

  .legend-title {
    font-size: 0.9rem;
  }

  .legend-items {
    gap: 1rem;
  }

  .legend-item {
    gap: 0.5rem;
  }

  .legend-text {
    font-size: 0.8rem;
  }

  .legend-count {
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
  }

  .map-chart {
    height: 400px;
    padding: 0.5rem;
  }

  .locations-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .location-card {
    border-radius: 8px;
  }

  .card-header {
    padding: 1rem;
  }

  .location-name {
    font-size: 1rem;
  }

  .threat-badge {
    padding: 0.3rem 0.6rem;
    font-size: 0.9rem;
  }

  .card-body {
    padding: 1rem;
  }

  .stat-row {
    padding: 0.6rem 0;
  }

  .stat-label {
    font-size: 0.85rem;
  }

  .stat-number {
    font-size: 1.3rem;
  }

  .card-footer {
    padding: 0.75rem 1rem;
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .last-update {
    font-size: 0.8rem;
  }

  .details-btn {
    width: 100%;
    padding: 0.6rem 1rem;
  }
}
</style>
