<template>
  <div class="logo">
    <div class="rest">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon" :width="w"
        :height="h">
        <image :xlink:href="detectUri()" :width="w"
          :height="h"></image>
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
    width: {
      type: Number,
      default: 290,
      required: false,
    },
    height: {
      type: Number,
      default: 35,
      required: false,
    },
  },
  data() {
    return {
      w: this.width,
      h: this.height,
    };
  },
  methods: {
    detectUri() {
      const name = this.short ? 'logo-short' : 'logo-full';
      return require(`@/assets/imgs/${name}.svg`);
    },
    scale(direction, size) {
      if (direction === 'up') {
        this.w = this.width * size;
        this.h = this.height * size;
      } else {
        this.w = this.width / size;
        this.h = this.height / size;
      }
    },
    manageSize() {
      if (this.short) {
        this.minimize();
      } else {
        this.normalSize();
      }
    },
    normalSize() {
      this.w = 290;
      this.h = 35;
    },
    minimize() {
      this.w = 35;
      this.h = 35;
    },
  },
  watch: {
    short: 'manageSize',
  },
  mounted() {
    this.scale('down', 1);
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.logo{
  color: $black;
  font-family: $title-font;
  font-size: 24px;
  height: auto;
  .rest{
    display: flex;
    justify-content: center;
    height: 100%;
  }
  &.invert{
    color: $green;
  }
  .icon{
    image {
      fill: $black;
      transition: all .4s ease-in;
    }
  }
}
</style>
