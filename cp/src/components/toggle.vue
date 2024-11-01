<template>
  <div class="toggle">
    <input type="checkbox" class="inv_input">
    <div class="toggle_thumbar" @click="checkMe">
      <div class="toggle_thumbar-thumb" :class="localChecked ? 'checked' : ''"></div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Toggle',
  model: {
    prop: 'checked',
    event: 'change',
  },
  props: {
    checked: {
      required: false,
      type: Boolean,
    },
  },
  emits: ['update:checked'],
  data() {
    return {
    };
  },
  methods: {
    checkMe() {
      this.localChecked = !this.localChecked;
    },
  },
  computed: {
    localChecked: {
      get() { return this.checked; },
      set(value) { this.$emit('update:checked', value); },
    },
  },
  mounted() {
    this.localChecked = this.checked;
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.toggle{
  margin: 0 5px;
  &_thumbar{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    width: 50px;
    height: 20px;
    background: $white;
    border-radius: 20px;
    box-shadow: $toggle-shadow;
    cursor: pointer;
    &:has(.toggle_thumbar-thumb.checked) {
      background: rgba(252, 231, 204, 0.3);
    }
    &-thumb{
      position: absolute;
      border-radius: 50%;
      background-color: $green;
      width: 26px;
      height: 26px;
      right: calc(100% - 26px);
      box-shadow: inset 0 0 5px 1px rgba(252, 231, 204, 0.1);
      transition: right .2s ease-in;
      &.checked{
        right: 0;
        box-shadow: inset 0 0 5px 1px rgba(252, 231, 204, 0.3);
      }
    }
  }
}
</style>
