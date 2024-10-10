<template>
  <div class="m-icon" :class="active ? 'active' : ''"
    ref="mainIcon" :width="width" :height="height" @click="$emit('click')">
    <svg :width="width" :height="height" xmlns="http://www.w3.org/2000/svg" class="icon">
      <image :xlink:href="detectUri" :width="width" :height="height" />
    </svg>
  </div>
</template>
<script>
export default {
  name: 'MIcons',
  props: {
    width: {
      type: Number,
      default: 35,
    },
    height: {
      type: Number,
      default: 35,
    },
    name: {
      type: String,
      required: true,
    },
    active: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {};
  },
  computed: {
    detectUri() {
      return require(`../assets/icons/${this.name}.svg`);
    },
  },
};
</script>
<style lang="scss" scoped>
.m-icon{
  box-sizing: border-box;
  display: flex;
  cursor: pointer;
  &.active{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
    width: 60px;
    background: transparent;
    border-radius: 50%;
  }
}
</style>
