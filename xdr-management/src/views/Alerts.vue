<template>
  <div class="alerts">
    <div class="card">
      <h2>Alert Rules</h2>
      <div class="rules-list">
        <div v-for="rule in rules" :key="rule.id" class="rule-card">
          <div class="rule-header">
            <h3>{{ rule.name }}</h3>
            <label class="toggle">
              <input type="checkbox" :checked="rule.enabled" />
              <span class="slider"></span>
            </label>
          </div>
          <div class="rule-body">
            <div class="rule-severity">
              <span class="severity-badge" :class="rule.severity">{{ rule.severity }}</span>
            </div>
            <div class="rule-condition">
              <strong>Conditions:</strong> {{ rule.conditions }}
            </div>
            <div class="rule-actions">
              <strong>Actions:</strong> {{ rule.actions.join(', ') }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useXdrStore } from '../stores/xdr'

const xdrStore = useXdrStore()
const rules = computed(() => xdrStore.rules)

// Load alert rules on mount
onMounted(async () => {
  await xdrStore.fetchAlertRules()
})
</script>

<style scoped>
.alerts {
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

.rules-list {
  margin-top: 1.5rem;
}

.rule-card {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.rule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.rule-header h3 {
  margin: 0;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #10b981;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.severity-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.severity-badge.critical {
  background: #fee2e2;
  color: #991b1b;
}

.severity-badge.high {
  background: #fef3c7;
  color: #92400e;
}

.rule-condition, .rule-actions {
  margin-top: 0.5rem;
  color: #6b7280;
}
</style>

/* Responsive */
@media (max-width: 1024px) {
  .alerts {
    padding: 1.5rem;
  }

  .rules-list {
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .alerts {
    padding: 1rem;
  }

  .card {
    padding: 1.5rem;
  }

  .rule-card {
    padding: 1rem;
  }

  .rule-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .rule-header h3 {
    font-size: 1rem;
  }

  .rule-condition,
  .rule-actions {
    font-size: 0.85rem;
  }
}
