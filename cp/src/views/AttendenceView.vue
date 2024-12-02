<template>
  <article class="attendance">
    <div class="attendance_filter" :class="mobile ? 'mobile' : ''">
      <FilterInput v-model:keyword="filterKey" />
    </div>
    <div class="attendance_table">
      <div class="attendance_table-wrapper" :class="mobile ? 'mobile' : ''">
        <div class="attendance_table-headers">
          <div class="attendance_table-th changable index_cell"></div>
          <div class="attendance_table-th changable">КЛИЕНТ</div>
          <div class="attendance_table-th changable event_cell">КУРС</div>
          <div class="attendance_table-th changable">ОПЛАТА</div>
        </div>
        <div class="attendance_table-body">
          <div class="attendance_table-row changable" v-for="(at, idx) in filteredResult"
            :key="at.uid" :ref="`atRow_${idx}`">
            <div class="attendance_table-data index_cell">{{ idx }}</div>
            <div class="attendance_table-data">{{ at.client.fullName }}</div>
            <div class="attendance_table-data event_cell">
              {{ at.event.name }} {{ prettyDate(at.event.date) }}
            </div>
            <div class="attendance_table-data payment">
              <PayForm :id="`payform_${at.uid}`" @payment="savePayment"
                @focus="makeVisible(idx)" select/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>
<script>
import Backend from '@/services/backend.service';
import PayForm from '@/components/paymentForm.vue';
import FilterInput from '@/components/filterInput.vue';
import '@/utils/date';

export default {
  name: 'AttendenceView',
  components: { PayForm, FilterInput },
  data() {
    return {
      backend: new Backend(),
      mobile: false,
      attendance: [],
      payments: [],
      paymentEl: {
        uid: null,
        type: {
          sub: false,
          cert: false,
        },
        price: null,
      },
      filterKey: null,
    };
  },
  methods: {
    getAllAttendances() {
      this.backend.get('/attendance')
        .then((resp) => {
          this.attendance = resp;
        })
        .catch((err) => console.error(err));
    },
    prettyDate(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.shortDate();
    },
    savePayment(form) {
      console.log(form);
      this.makeInvisible();
    },
    makeVisible(idx) {
      const obj = this.$refs[`atRow_${idx}`][0];
      if (this.currentRow) {
        this.currentRow.classList.remove('opened');
      }
      this.currentRow = obj;
      obj.classList.add('opened');
    },
    makeInvisible() {
      if (this.currentRow) {
        this.currentRow.classList.remove('opened');
        this.currentRow = null;
      }
    },
    paymentPresent(uid) {
      this.payments.forEach((obj) => (obj ? obj.attendanceUid === uid : false));
    },
    searchInObject(obj, kwd) {
      return Object.values(obj).some((value) => {
        if (typeof value === 'object' && value !== null) {
          return this.searchInObject(value, kwd);
        }
        return `${value}`.toLowerCase().includes(kwd);
      });
    },
  },
  computed: {
    filteredResult() {
      const searchableKeys = ['client', 'event', 'uid'];

      return this.attendance.filter((at) => {
        if (!this.filterKey) return true;
        const keyword = this.filterKey.toLowerCase();
        return searchableKeys.some((key) => {
          const value = at[key];
          if (typeof value === 'object' && value !== null) {
            return this.searchInObject(value, keyword);
          }
          return `${value}`.toLowerCase().includes(keyword);
        });
      });
    },
  },
  mounted() {
    this.filterKey = this.$route.query.uid ? this.$route.query.uid : null;
    this.getAllAttendances();
    this.mobile = this.$isMobile();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.attendance{
  overflow: hidden;
  &_filter{
    display: flex;
    max-width: 350px;
    width: 100%;
    &.mobile{
      max-width: 100%;
    }
  }
  &_table{
    overflow-x: auto;
    font-family: $text-font;
    display: flex;
    padding: 0 20px;
    .event_cell{
      min-width: 160px;
      max-width: 160px;
    }
    .index_cell{
      max-width: auto;
      min-width: auto;
      padding: 0 10px;
      display: flex;
      align-items: center;
    }
    .price_cell{
      display: none;
      max-width: 250px;
    }
    &-headers{
      display: flex;
      font-weight: bold;
    }
    &-th{
      min-width: 200px;
      text-align: center;
      padding: 10px 0;
    }
    &-row{
      display: flex;
      padding: 5px;
      margin-bottom: 5px;
      height: 45px;
      &:hover{
        .attendance_table-data.payment{
          display: block;
        }
      }
      &.opened{
        .attendance_table-data.payment{
          display: block;
        }
      }
    }
    &-data{
      min-width: 200px;
      max-width: 200px;
      display: flex;
      align-items: center;
      user-select: none;
      &.payment{
        display: none;
      }
    }
  }
}
</style>
