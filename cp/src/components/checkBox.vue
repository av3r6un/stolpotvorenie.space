<template>
  <div class="checkbox">
    <input type="checkbox" class="inv_input input_checkbox" :id="id" v-model="localChecked">
    <div class="checkbox_checkbox" @click="toggleCheck">
      <div class="checkbox_check" :class="localChecked ? 'checked': ''"></div>
      <div class="checkbox_placeholder">{{ placeholder }}</div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'CheckBox',
  model: {
    prop: 'checked',
    event: 'input',
  },
  props: {
    checked: {
      type: Boolean,
      required: false,
    },
    id: {
      type: String,
      default: 'check',
      required: false,
    },
    placeholder: {
      type: String,
      required: false,
    },
  },
  emits: ['update:checked'],
  data() {
    return {};
  },
  methods: {
    toggleCheck() {
      this.localChecked = !this.checked;
    },
  },
  computed: {
    localChecked: {
      get() { return this.checked; },
      set(value) { this.$emit('update:checked', value); },
    },
  },
  mounted() {},
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.checkbox{
  display: flex;
  &_checkbox{
    position: relative;
    width: 35px;
    height: 35px;
    border-radius: 7px;
    background: rgba($color: $white, $alpha: .8);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  &_check{
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 35px;
    height: 35px;
    &.checked{
      box-shadow: inset 1px 1px 10px rgba($color: $green, $alpha: .8);
      border-radius: 7px;
    }
    &.checked:after{
      position: absolute;
      left: calc(50% - 8.75px);
      top: calc(50% - 10.5px);
      content: '\f00c';
      font-family: 'FontAwesome';
      font-size: 20px;
      color: $green;
      z-index: 2;
    }
  }
}
</style>
