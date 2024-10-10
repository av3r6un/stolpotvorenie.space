<template>
  <div class="checkbox">
    <input type="checkbox" class="inv_input" :id="id"
      @change="toggleState" v-model="this.checked">
      <div class="checkbox_checkbox" :class="checked ? 'checked' : ''"
        @click="toggleState">
      </div>
      <label :for="id" class="checkbox_label" v-if="name">{{ name }}</label>
  </div>
</template>
<script>
export default {
  props: {
    name: {
      type: String,
      required: false,
    },
    id: {
      type: String,
      required: true,
    },
    prechecked: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  name: 'checkBox',
  data() {
    return {
      checked: false,
    };
  },
  methods: {
    sendState() {
      this.$emit('input', this.checked);
    },
    toggleState() {
      this.checked = !this.checked;
      this.sendState();
    },
  },
  mounted() {
    this.checked = this.prechecked;
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.checkbox{
  display: flex;
  align-items: center;
  font-family: $text-font;
  color: $white;
  font-size: 16px;
  &_checkbox{
    height: 25px;
    width: 25px;
    border-radius: 8px;
    background: $semi-white;
    box-shadow: 0px 0px 5px rgba($color: $white, $alpha: .3);
    &.checked{
      position: relative;
      &:after{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        content: '\f00c';
        font-family: 'FontAwesome';
        color: $green;
        font-size: 20px;
      }
    }
  }
  &_label{
    color: $black;
    font-weight: 600;
    margin-left: 10px;
    user-select: none;
  }
}
</style>
