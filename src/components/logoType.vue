<template>
  <div class="logo">
    <span class="serif"></span>
    <div class="rest" v-if="!short">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon" :width="width"
        :height="height">
        <image :xlink:href="detectUri()" :width="width"
          :height="height"></image>
      </svg>
    </div>
  </div>
</template>
<script>
export default {
  name: 'logoType',
  props: {
    short: {
      type: Boolean,
      default: false,
    },
    inverted: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      width: 290,
      height: 25,
    };
  },
  methods: {
    detectUri() {
      const name = this.inverted ? 'logo-full' : 'logo-inverted';
      return require(`../assets/imgs/${name}.svg`);
    },
    scale(direction, size) {
      if (direction === 'up') {
        this.width *= size;
        this.height *= size;
      } else {
        this.width /= 2;
        this.height /= 2;
      }
    },
  },
  mounted() {
    this.scale('down', 2);
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.logo{
  color: $black;
  font-family: $title-font;
  font-size: 24px;
  &.invert{
    color: $green;
  }
  .icon{
    image {
      fill: $black;
    }
  }
}
</style>
