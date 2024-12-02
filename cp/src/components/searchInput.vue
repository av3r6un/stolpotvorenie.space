<template>
  <div class="input_search"></div>
</template>
<script>
export default {
  name: 'SearchInput',
  model: {
    prop: 'selected',
    event: 'input',
  },
  emits: ['update:selected'],
  props: {
    all: {
      type: Array,
      required: true,
    },
    selected: {
      required: false,
    },
  },
  data() {
    return {
      opened: false,
      localText: null,
    };
  },
  computed: {
    localSelected: {
      get() { return this.selected; },
      set(value) { this.$emit('update:selected', value); },
    },
  },
  methods: {
    toggleDropdown() {},
    selectOption() {},
    reset() {
      this.localSelected = null,
      this.localText = null;
    },
  },
  mounted() {
    this.localSelected = this.selected;
  },
}
</script>
