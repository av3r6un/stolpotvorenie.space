<template>
  <div class="payment">
    <form class="payment_form" @submit.prevent="emitResult" :id="id">
      <div class="input_price">
        <i class="fa">₽</i>
        <input type="number" class="input_wide small_input" v-model="form.price"
          @focus="$emit('focus')">
      </div>
      <CheckBox placeholder="A" v-model:checked="form.subscription" @click="validateSibling('a')" />
      <CheckBox placeholder="C" v-model:checked="form.certificate" @click="validateSibling('c')" />
      <button type="submit" class="btn btn_small"><i class="fa check"></i></button>
    </form>
  </div>
</template>
<script>
import CheckBox from './checkBox.vue';

export default {
  name: 'PayForm',
  components: { CheckBox },
  props: {
    id: {
      type: String,
      required: true,
    },
    select: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      form: {
        price: null,
        subscription: null,
        certificate: null,
      },
    };
  },
  methods: {
    emitResult() {
      this.$emit('payment', this.form);
    },
    validateSibling(type) {
      this.$emit('focus');
      const types = {
        a: {
          text: 'subscription',
          obj: this.form.subscription,
          opposite: 'certificate',
        },
        c: {
          text: 'certificate',
          obj: this.form.certificate,
          opposite: 'subscription',
        },
      };
      if (this.select) {
        const current = types[type];
        this.form[current.opposite] = !current.obj ? false : !current.obj;
      }
    },
  },
  mounted() {},
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.payment{
  &_form{
    display: flex;
    .checkbox{
      margin-left: 10px;
      &:last-child{
        margin-right: 0;
      }
    }
    .input_price{
      display: flex;
      position: relative;
      .input_wide{
        margin-bottom: 0;
      }
      .small_input{
        padding-right: 10px;
        direction: rtl;
        &::-webkit-inner-spin-button,
        &::-webkit-outer-spin-button{
          -webkit-appearance: none;
          margin: 0;
        }
      }
      i{
        position: absolute;
        left: 7px;
        top: calc(50% - 7.5px);
        font-weight: normal;
        width: 15px;
        height: 15px;
      }
    }
    .input_checkbox{
      display: flex;
      background: rgba($color: $white, $alpha: .3);
      border-radius: 7px;
      width: 35px;
      height: 35px;
      .input_wide{
        width: auto;
      }
    }
  }
}
</style>
