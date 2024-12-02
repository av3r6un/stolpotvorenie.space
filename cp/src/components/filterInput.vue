<template>
  <div class="filter">
    <input type="text" class="input_wide filter_input"
      :placeholder="placeholder" v-model="localKeyword">
    <div class="clear_button" @click="clearInput"></div>
  </div>
</template>
<script>
export default {
  name: 'FilterInput',
  model: {
    prop: 'keyword',
    event: 'input',
  },
  props: {
    keyword: {
      type: String,
    },
    placeholder: {
      type: String,
      required: false,
      default: 'Поиск',
    },
  },
  emits: ['update:keyword'],
  data() {
    return {};
  },
  computed: {
    localKeyword: {
      get() { return this.keyword; },
      set(value) { this.$emit('update:keyword', value); },
    },
  },
  methods: {
    clearInput() {
      this.localKeyword = null;
    },
  },
  mounted() {
    this.localKeyword = this.keyword;
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.filter{
  position: relative;
  display: flex;
  width: 100%;
  &_input{
    border: 1px solid transparent;
    &:not(:placeholder-shown){
      border: 1px solid $green;
      & + .clear_button{
        display: flex;
      }
    }
  }
  .clear_button{
    display: none;
    height: 35px;
    width: 35px;
    position: absolute;
    align-items: center;
    justify-content: center;
    right: 0px;
    cursor: pointer;
    &:after{
      content: '\f057';
      position: absolute;
      font-family: 'FontAwesome';
      color: $green;
    }
  }
}
</style>
