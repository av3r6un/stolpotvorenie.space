<template>
  <div class="input_dropdown" @click="toggleDropdown">
    <div class="input_dropdown-selected">
      <input type="text" readonly class="input_wide" :placeholder="placeholder"
        v-model="localText">
      <div class="input_dropdown-icon" :class="opened ? 'opened' : ''">
        <div class="chevron_bottom"></div>
      </div>
    </div>
    <div class="input_dropdown-options" v-show="opened" v-if="nested">
      <div class="input_dropdown-option" v-for="option in options" :key="option.uid"
        @click="selectNestedOption(option)">{{ option[nestedParam] }}</div>
    </div>
    <div class="input_dropdown-options" v-show="opened" v-else-if="indexed">
      <div class="input_dropdown-option" v-for="option, idx in options" :key="idx"
        @click="selectIndexedOption(option, idx)">{{ option }}</div>
    </div>
    <div class="input_dropdown-options" v-show="opened" v-else-if="seminested">
      <div class="input_dropdown-option" v-for="name, option in options" :key="option"
        @click="selectSemiNestedOption(option, name)">{{ name }}</div>
    </div>
    <div class="input_dropdown-options" v-show="opened" v-else-if="unique">
      <div class="input_dropdown-option" v-for="option in options" :key="option.id"
        @click="selectUniqueOption(option)">{{ option.name }}</div>
    </div>
    <div class="input_dropdown-options" v-show="opened" v-else>
      <div class="input_dropdown-option" v-for="option, idx in options" :key="idx"
        @click="selectOption(option)">{{ option }}</div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'dropDown',
  model: {
    prop: 'selected',
    event: 'input',
  },
  props: {
    options: {
      required: true,
    },
    placeholder: {
      type: String,
      required: false,
      default: 'Выберите из списка',
    },
    selected: {
      required: false,
    },
    nested: {
      type: Boolean,
      default: false,
      required: false,
    },
    nestedParam: {
      type: String,
      required: false,
      default: 'name',
    },
    indexed: {
      type: Boolean,
      default: false,
      required: false,
    },
    seminested: {
      type: Boolean,
      default: false,
      required: false,
    },
    unique: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  emits: ['update:selected'],
  data() {
    return {
      opened: false,
      localText: null,
    };
  },
  methods: {
    toggleDropdown() {
      this.opened = !this.opened;
    },
    selectOption(value) {
      this.localSelected = value;
      this.localText = value;
    },
    selectNestedOption(option) {
      this.localSelected = option.uid;
      this.localText = option[this.nestedParam];
    },
    selectIndexedOption(option, idx) {
      this.localSelected = idx;
      this.localText = option;
    },
    selectUniqueOption(option) {
      this.localSelected = option.id;
      this.localText = option.name;
    },
    selectSemiNestedOption(option, name) {
      this.localSelected = option;
      this.localText = name;
    },
    reset() {
      this.localSelected = null;
      this.localText = null;
    },
  },
  computed: {
    localSelected: {
      get() { return this.selected; },
      set(value) { this.$emit('update:selected', value); },
    },
  },
  mounted() {
    this.localSelected = this.selected;
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.input_dropdown{
  position: relative;
  .input_wide{
    user-select: none;
    cursor: pointer;
  }
  &-icon{
    &.opened{
      transform: rotateX(180deg);
    }
    position: absolute;
    right: 10px;
    top: 5px;
    color: $semi-black;
    transition: transform .4s ease-in;
  }
  &-selected{
    position: relative;
  }
  &-options{
    position: absolute;
    z-index: 3;
    top: 35px;
    width: 100%;
    max-height: 180px;
    overflow-y: auto;
    &::-webkit-scrollbar{
      -webkit-appearance: none;
      width: 4px;
      &-thumb{
        width: 4px;
        background: rgba($color: $semi-black, $alpha: .2);
        border-radius: 4px;
      }
    }
    background: $semi-white;
    border-radius: 7px;
    font-family: $text-font;
    color: $semi-black;
    box-shadow: 0px 5px 5px rgba($color: $semi-black, $alpha: .3);
  }
  &-option{
    height: 25px;
    text-align: center;
    width: 100%;
    line-height: 25px;
    cursor: pointer;
    &:hover{
      background: rgba($color: $semi-black, $alpha: .2);
      &:first-child{
        border-radius: 7px 7px 0 0;
      }
      &:last-child{
        border-radius: 0 0 7px 7px;
      }
    }
  }
}
</style>
