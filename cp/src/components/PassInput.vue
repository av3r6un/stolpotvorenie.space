<template>
  <div class="pass_input">
    <input type="password" class="input_wide" autocomplete="off"
      :required="required" :placeholder="placeholder" ref="mainInput"
      v-model="localText">
    <div class="reveal fa" :class="revealed ? 'fa-unveal' : 'fa-reveal'"
      @click="revealPassword"></div>
  </div>
</template>
<script>
export default {
  name: 'PassInput',
  model: {
    prop: 'text',
    event: 'input',
  },
  props: {
    text: {
      required: false,
      type: String,
    },
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    placeholder: {
      type: String,
      required: false,
      default: '',
    },
  },
  emits: ['update:text'],
  data() {
    return {
      revealed: false,
    };
  },
  computed: {
    localText: {
      get() { return this.text; },
      set(value) { this.$emit('update:text', value); },
    },
  },
  methods: {
    revealPassword() {
      this.$refs.mainInput.type = this.revealed ? 'password' : 'text';
      this.revealed = !this.revealed;
    },
  },
  mounted() {},
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.pass_input{
  position: relative;
  width: 100%;
  margin-bottom: 10px;
  border-radius: 8px;
  &:last-of-type{
    margin-bottom: 0;
  }
  .reveal{
    position: absolute;
    right: 10px;
    top: calc(50% - 12.5px);
    color: $semi-black;
  }
  .input_wide{
    margin-bottom: 0;
  }
}
</style>
