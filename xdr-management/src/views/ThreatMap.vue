<template>
  <div class="threat-map">
    <div class="map-header">
      <div class="header-left">
        <h1>3D Geographic Threat Map</h1>
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
        <div class="filter-group">
          <label>View Mode:</label>
          <select v-model="viewMode" class="filter-select">
            <option value="3d">3D Bar View</option>
            <option value="scatter">3D Scatter View</option>
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
      <div class="view-controls">
        <span class="control-hint">Drag to rotate | Scroll to zoom | Right-click to pan</span>
      </div>
    </div>

    <!-- Main 3D Map Visualization -->
    <div class="map-container">
      <div class="map-chart" ref="mapChartRef">
        <v-chart
          v-if="chartReady"
          :key="chartKey"
          :option="mapOption"
          autoresize
          @click="handleLocationClick"
        />
        <div v-else class="chart-loading">
          <span>Loading 3D Map...</span>
        </div>
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
            <span class="location-icon">{{ getLocationIcon(location) }}</span>
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
            View Details
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import VChart from 'vue-echarts'
import * as echarts from 'echarts'
import 'echarts-gl'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

// Chart control
const chartReady = ref(true)
const chartKey = ref(0)

// South Korea GeoJSON with provinces
const koreaGeoJson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Seoul" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[126.8, 37.7], [127.2, 37.7], [127.2, 37.4], [126.8, 37.4], [126.8, 37.7]]]
      }
    },
    {
      "type": "Feature",
      "properties": { "name": "Gyeonggi" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[126.3, 38.0], [127.8, 38.0], [127.8, 36.9], [126.3, 36.9], [126.3, 38.0]]]
      }
    },
    {
      "type": "Feature",
      "properties": { "name": "Gangwon" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[127.5, 38.5], [129.3, 38.5], [129.3, 37.0], [127.5, 37.0], [127.5, 38.5]]]
      }
    },
    {
      "type": "Feature",
      "properties": { "name": "Chungcheong" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[126.0, 37.0], [128.0, 37.0], [128.0, 35.9], [126.0, 35.9], [126.0, 37.0]]]
      }
    },
    {
      "type": "Feature",
      "properties": { "name": "Jeolla" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[126.0, 36.0], [127.8, 36.0], [127.8, 34.3], [126.0, 34.3], [126.0, 36.0]]]
      }
    },
    {
      "type": "Feature",
      "properties": { "name": "Gyeongsang" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[127.8, 37.0], [129.6, 37.0], [129.6, 34.8], [127.8, 34.8], [127.8, 37.0]]]
      }
    },
    {
      "type": "Feature",
      "properties": { "name": "Jeju" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[126.1, 33.6], [126.9, 33.6], [126.9, 33.2], [126.1, 33.2], [126.1, 33.6]]]
      }
    }
  ]
}

// Register South Korea map
echarts.registerMap('SouthKorea', koreaGeoJson)

const router = useRouter()
const timeRange = ref('24h')
const threatFilter = ref('all')
const viewMode = ref('3d')
const mapChartRef = ref(null)

// Watch viewMode changes and recreate chart
watch(viewMode, async () => {
  chartReady.value = false
  await nextTick()
  chartKey.value++
  await nextTick()
  setTimeout(() => {
    chartReady.value = true
  }, 300)
})

// Location data with actual Korean city coordinates (longitude, latitude)
const locations = ref([
  {
    name: 'Seoul HQ',
    coord: [126.9780, 37.5665],
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
    coord: [129.0756, 35.1796],
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
    coord: [126.7052, 37.4563],
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
    coord: [128.6014, 35.8714],
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
    coord: [127.3845, 36.3504],
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
    coord: [126.8526, 35.1595],
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
    coord: [129.3114, 35.5384],
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
    coord: [127.0286, 37.2636],
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
    coord: [126.5312, 33.4996],
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
    coord: [128.6811, 35.2280],
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

const getLocationIcon = (location) => {
  const level = getThreatLevel(location.threats)
  if (level === 'critical') return '🔴'
  if (level === 'high') return '🟠'
  if (level === 'medium') return '🔵'
  return '🟢'
}

// 3D Map Option
const map3DOption = computed(() => ({
  backgroundColor: '#0a1628',
  tooltip: {
    show: true,
    formatter: (params) => {
      if (!params.data || !params.data.name) return ''
      const loc = locations.value.find(l => l.name === params.data.name)
      if (!loc) return params.data.name
      return `<div style="padding: 12px; min-width: 200px; background: rgba(10, 22, 40, 0.95); border-radius: 8px;">
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #fff;">
          ${getLocationIcon(loc)} ${loc.name}
        </div>
        <div style="display: grid; gap: 4px;">
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Events:</span>
            <strong style="color: #fff;">${loc.events}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Threats:</span>
            <strong style="color: ${getThreatColor(loc.threats)};">${loc.threats}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Active:</span>
            <strong style="color: #ef4444;">${loc.activeThreats}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Incidents:</span>
            <strong style="color: #fff;">${loc.incidents}</strong>
          </div>
        </div>
      </div>`
    },
    backgroundColor: 'transparent',
    borderWidth: 0,
    textStyle: { color: '#fff' }
  },
  geo3D: {
    map: 'SouthKorea',
    roam: true,
    regionHeight: 2,
    viewControl: {
      autoRotate: false,
      autoRotateSpeed: 5,
      distance: 100,
      alpha: 40,
      beta: 0,
      minAlpha: 5,
      maxAlpha: 90,
      minBeta: -360,
      maxBeta: 360,
      animation: true,
      animationDurationUpdate: 1000,
      animationEasingUpdate: 'cubicInOut'
    },
    shading: 'realistic',
    realisticMaterial: {
      roughness: 0.6,
      metalness: 0.1
    },
    postEffect: {
      enable: true,
      bloom: {
        enable: true,
        intensity: 0.1
      },
      SSAO: {
        enable: true,
        radius: 2,
        intensity: 1
      }
    },
    light: {
      main: {
        intensity: 1.2,
        shadow: true,
        shadowQuality: 'high',
        alpha: 55,
        beta: 10
      },
      ambient: {
        intensity: 0.3
      }
    },
    groundPlane: {
      show: true,
      color: '#0a1628'
    },
    itemStyle: {
      color: '#1e3a5f',
      borderWidth: 1,
      borderColor: '#3b82f6'
    },
    emphasis: {
      itemStyle: {
        color: '#2563eb'
      },
      label: {
        show: false
      }
    },
    label: {
      show: false
    }
  },
  series: [
    // 3D Bar for threat levels at each location
    {
      name: 'Threat Bars',
      type: 'bar3D',
      coordinateSystem: 'geo3D',
      barSize: 0.8,
      shading: 'realistic',
      minHeight: 0.5,
      silent: false,
      data: filteredLocations.value.map(loc => ({
        name: loc.name,
        value: [loc.coord[0], loc.coord[1], loc.threats / 5],
        itemStyle: {
          color: getThreatColor(loc.threats),
          opacity: 0.9
        },
        emphasis: {
          itemStyle: {
            color: '#fff'
          }
        }
      })),
      label: {
        show: true,
        position: 'top',
        formatter: (params) => params.data.name,
        textStyle: {
          color: '#fff',
          fontSize: 11,
          fontWeight: 'bold',
          backgroundColor: 'rgba(0, 0, 0, 0.6)',
          padding: [4, 8],
          borderRadius: 4
        }
      }
    },
    // Scatter3D for location points
    {
      name: 'Locations',
      type: 'scatter3D',
      coordinateSystem: 'geo3D',
      symbolSize: (val) => {
        const size = val[2] * 0.3
        return Math.max(size, 12)
      },
      data: filteredLocations.value.map(loc => ({
        name: loc.name,
        value: [loc.coord[0], loc.coord[1], loc.threats / 5 + 1],
        itemStyle: {
          color: getThreatColor(loc.threats),
          borderColor: '#fff',
          borderWidth: 2
        }
      })),
      label: {
        show: false
      }
    },
    // Lines3D for connections from Seoul HQ
    {
      name: 'Connections',
      type: 'lines3D',
      coordinateSystem: 'geo3D',
      effect: {
        show: true,
        period: 3,
        trailLength: 0.2,
        trailWidth: 3,
        trailOpacity: 0.6,
        trailColor: '#60a5fa'
      },
      lineStyle: {
        color: '#3b82f6',
        width: 1,
        opacity: 0.4
      },
      blendMode: 'lighter',
      data: filteredLocations.value
        .filter(loc => loc.name !== 'Seoul HQ')
        .map(loc => {
          const seoulLoc = locations.value.find(l => l.name === 'Seoul HQ')
          return {
            coords: [
              [seoulLoc.coord[0], seoulLoc.coord[1], seoulLoc.threats / 5 + 1],
              [loc.coord[0], loc.coord[1], loc.threats / 5 + 1]
            ]
          }
        })
    }
  ]
}))

// 3D Scatter view option (alternative view)
const scatterOption = computed(() => ({
  backgroundColor: '#0a1628',
  tooltip: {
    show: true,
    formatter: (params) => {
      if (!params.data || !params.data.name) return ''
      const loc = locations.value.find(l => l.name === params.data.name)
      if (!loc) return params.data.name
      return `<div style="padding: 12px; min-width: 200px; background: rgba(10, 22, 40, 0.95); border-radius: 8px;">
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #fff;">
          ${getLocationIcon(loc)} ${loc.name}
        </div>
        <div style="display: grid; gap: 4px;">
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Events:</span>
            <strong style="color: #fff;">${loc.events}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Threats:</span>
            <strong style="color: ${getThreatColor(loc.threats)};">${loc.threats}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Active:</span>
            <strong style="color: #ef4444;">${loc.activeThreats}</strong>
          </div>
        </div>
      </div>`
    },
    backgroundColor: 'transparent',
    borderWidth: 0,
    textStyle: { color: '#fff' }
  },
  geo3D: {
    map: 'SouthKorea',
    roam: true,
    regionHeight: 1,
    viewControl: {
      autoRotate: true,
      autoRotateSpeed: 3,
      distance: 120,
      alpha: 50,
      beta: 30,
      animation: true
    },
    shading: 'realistic',
    realisticMaterial: {
      roughness: 0.7,
      metalness: 0
    },
    postEffect: {
      enable: true,
      bloom: {
        enable: true,
        intensity: 0.15
      }
    },
    light: {
      main: {
        intensity: 1.5,
        shadow: true,
        shadowQuality: 'high',
        alpha: 40,
        beta: 30
      },
      ambient: {
        intensity: 0.4
      }
    },
    itemStyle: {
      color: '#1e3a5f',
      borderWidth: 1,
      borderColor: '#60a5fa'
    },
    emphasis: {
      itemStyle: {
        color: '#3b82f6'
      }
    }
  },
  series: [
    // Large scatter points with glow effect
    {
      name: 'Threat Points',
      type: 'scatter3D',
      coordinateSystem: 'geo3D',
      symbol: 'circle',
      symbolSize: (val) => {
        return Math.max(val[2] * 0.4, 15)
      },
      data: filteredLocations.value.map(loc => ({
        name: loc.name,
        value: [loc.coord[0], loc.coord[1], loc.threats / 3],
        itemStyle: {
          color: getThreatColor(loc.threats),
          borderColor: '#fff',
          borderWidth: 2,
          opacity: 0.9
        }
      })),
      label: {
        show: true,
        position: 'top',
        formatter: (params) => `${params.data.name}\n${locations.value.find(l => l.name === params.data.name)?.threats || 0}`,
        textStyle: {
          color: '#fff',
          fontSize: 11,
          fontWeight: 'bold',
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          padding: [6, 10],
          borderRadius: 4
        },
        distance: 15
      }
    },
    // Animated connection lines
    {
      name: 'Connections',
      type: 'lines3D',
      coordinateSystem: 'geo3D',
      effect: {
        show: true,
        period: 2.5,
        trailLength: 0.3,
        trailWidth: 4,
        trailOpacity: 0.8,
        trailColor: '#60a5fa'
      },
      lineStyle: {
        color: '#3b82f6',
        width: 2,
        opacity: 0.5
      },
      blendMode: 'lighter',
      data: filteredLocations.value
        .filter(loc => loc.name !== 'Seoul HQ')
        .map(loc => {
          const seoulLoc = locations.value.find(l => l.name === 'Seoul HQ')
          return {
            coords: [
              [seoulLoc.coord[0], seoulLoc.coord[1], seoulLoc.threats / 3],
              [loc.coord[0], loc.coord[1], loc.threats / 3]
            ]
          }
        })
    }
  ]
}))

const mapOption = computed(() => {
  return viewMode.value === 'scatter' ? scatterOption.value : map3DOption.value
})

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
  console.log('3D Threat Map loaded')
})
</script>

<style scoped>
.threat-map {
  padding: 2rem;
  background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 100%);
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
  color: #fff;
  text-shadow: 0 2px 10px rgba(59, 130, 246, 0.5);
}

.subtitle {
  margin: 0.5rem 0 0 0;
  color: #94a3b8;
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
  color: #94a3b8;
}

.filter-select {
  padding: 0.6rem 1rem;
  border: 1px solid #3b82f6;
  border-radius: 8px;
  background: rgba(30, 58, 95, 0.8);
  color: #fff;
  font-size: 0.9rem;
  cursor: pointer;
  min-width: 150px;
  transition: all 0.3s;
}

.filter-select:hover {
  border-color: #60a5fa;
  background: rgba(59, 130, 246, 0.2);
}

.filter-select:focus {
  outline: none;
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.filter-select option {
  background: #1e3a5f;
  color: #fff;
}

.map-legend-section {
  background: rgba(30, 58, 95, 0.6);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  margin-bottom: 2rem;
}

.legend-title {
  font-weight: 700;
  font-size: 1rem;
  color: #fff;
  margin-bottom: 1rem;
}

.legend-items {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
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
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 10px currentColor;
}

.legend-marker.critical {
  background: #ef4444;
  box-shadow: 0 0 15px #ef4444;
}

.legend-marker.high {
  background: #f59e0b;
  box-shadow: 0 0 15px #f59e0b;
}

.legend-marker.medium {
  background: #3b82f6;
  box-shadow: 0 0 15px #3b82f6;
}

.legend-marker.low {
  background: #10b981;
  box-shadow: 0 0 15px #10b981;
}

.legend-text {
  font-size: 0.9rem;
  color: #94a3b8;
}

.legend-count {
  font-weight: 700;
  color: #fff;
  background: rgba(59, 130, 246, 0.3);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

.view-controls {
  border-top: 1px solid rgba(59, 130, 246, 0.2);
  padding-top: 1rem;
}

.control-hint {
  font-size: 0.85rem;
  color: #64748b;
}

.map-container {
  background: rgba(10, 22, 40, 0.9);
  border-radius: 16px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  overflow: hidden;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.map-chart {
  height: 600px;
}

.chart-loading {
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 1.2rem;
}

.locations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.location-card {
  background: rgba(30, 58, 95, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-left: 4px solid;
  transition: all 0.3s ease;
  cursor: pointer;
}

.location-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
  border-color: rgba(59, 130, 246, 0.5);
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
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
}

.location-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.location-icon {
  font-size: 1rem;
}

.threat-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
}

.threat-badge.critical {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid #ef4444;
}

.threat-badge.high {
  background: rgba(245, 158, 11, 0.2);
  color: #fcd34d;
  border: 1px solid #f59e0b;
}

.threat-badge.medium {
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
  border: 1px solid #3b82f6;
}

.threat-badge.low {
  background: rgba(16, 185, 129, 0.2);
  color: #6ee7b7;
  border: 1px solid #10b981;
}

.card-body {
  padding: 1.25rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-label {
  color: #94a3b8;
  font-size: 0.9rem;
}

.stat-value {
  font-weight: 700;
  color: #fff;
}

.stat-value.threat {
  color: #fca5a5;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background: rgba(10, 22, 40, 0.5);
  border-top: 1px solid rgba(59, 130, 246, 0.1);
}

.last-update {
  font-size: 0.85rem;
  color: #64748b;
}

.details-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.details-btn:hover {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
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
    min-width: auto;
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

  .map-legend-section {
    padding: 1rem;
  }

  .legend-items {
    gap: 1rem;
  }

  .legend-text {
    font-size: 0.8rem;
  }

  .map-chart {
    height: 400px;
  }

  .locations-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .card-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .details-btn {
    width: 100%;
  }
}
</style>
