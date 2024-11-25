<template>
  <div class="calendar changable" @mouseup.prevent="handlePages">
    <div class="calendar_year changable" v-if="calendarYear != currentYear">{{ calendarYear }}</div>
    <div class="calendar_wrapper changable">
      <div class="calendar_time changable" v-for="time, idx in times" :key="idx">{{ time }}</div>
      <div class="calendar_day changable empty">
        <div class="previous_week" @click="previousWeek"><i class="left_arrow"></i></div>
        <div class="current_week" @click="currentWeek" v-if="diff != 0">Сегодня</div>
        <div class="next_week" @click="nextWeek"><i class="right_arrow"></i></div>
      </div>
      <div class="calendar_day changable" v-for="(day, idx) in daysOfWeek" :key="idx">
        <div class="calendar_days-title">
          {{ day.format('dddd') }},<br> {{ day.format('D MMM') }}
        </div>
      </div>
      <div class="calendar_event" :class="event.type" v-for="event in events"
        :style="getEventStyle(event)" :key="event.uid"
        @click="selectEvent(event)" v-show="thisWeek(event)">
        <span class="calendar_event-name">{{ event.name }}</span>
        <span class="calendar_event-type" v-if="event.type">
          ({{ event.age }}+)
        </span>
      </div>
    </div>
    <transition name="appear-right">
      <div class="event_wrapper" v-show="selectedEvent" v-if="selectedEvent">
        <div class="event_wrapper-close" @click="selectedEvent = null">
          <div class="fa xmark changable"></div>
        </div>
        <div class="event_body">
          <div class="event_body-header">
            <div class="event_body-title">{{ selectedEvent.name }}</div>
            <div class="event_body-date" v-if="selectedEvent.type === 'event'">
              {{ selectedEventTiming }}
            </div>
            <div class="event_body-date" v-else>
              {{ this.initialDays[selectedEvent.day + 1] }}
              {{ selectedEvent.time.start }}-{{ selectedEvent.time.end }}
            </div>
          </div>
          <div class="event_body-teacher">
            <mIcon name="teachers" />
            {{ selectedEvent.executive.fullName }}
          </div>
          <div class="event_body-clients"></div>
          <div class="event_body-add_client">
            <form @submit.prevent="addAttendance" class="add_client-form">
              <dropDown :options="clients" placeholder="Выбрать клиента"
                nested nested-param="fullName"/>
              <button type="submit" class="btn">
                <mIcon name="plus-sign" :width="24" :height="24" />
              </button>
            </form>
          </div>
          <!-- <div class="event_body-comment" v-if="selectEvent.type === 'event'">
            {{ selectedEvent.comment }}
          </div>
          <div class="event_body-description" v-else>{{ selectedEvent.description }}<br>
            {{ selectedEvent.info }}
          </div> -->
          <div class="event_body-actions">
            <button class="btn btn_submit" type="button"
              @click="cancelEvent">Отменить</button>
            <button class="btn btn_submit delete" type="button"
              @click="deleteEvent" v-if="accessibleForDelete">Удалить</button>
            </div>
        </div>
      </div>
    </transition>
  </div>
</template>
<script>
import moment from 'moment';
import '@/utils/date';
import dropDown from '@/components/dropDown.vue';
import mIcon from '@/components/materialIcon.vue';

export default {
  name: 'Cal',
  components: { mIcon, dropDown },
  props: {
    dismissed: {
      type: Array,
      required: true,
    },
    events: {
      type: Array,
      required: true,
    },
    hourStart: {
      type: Number,
      default: 11,
      required: false,
    },
    hourEnd: {
      type: Number,
      default: 22,
      required: false,
    },
    hourGap: {
      type: Number,
      default: 30,
      required: false,
    },
    clients: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      currentDate: moment(),
      selectedEvent: null,
      initialDays: ['', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
      times: this.generateTimeSlots(),
      currentYear: new Date().getFullYear(),
      diff: 0,
      selectedEventWeek: null,
      localStorage: this.$parent.$parent.$parent.localStorage,
    };
  },
  methods: {
    generateTimeSlots() {
      const times = [];
      let startMinute = 0;
      let startHour = this.hourStart;
      const endHour = this.hourEnd;
      const endMinute = 0;

      while (startHour < endHour || (startHour === endHour && startMinute <= endMinute)) {
        const minutes = startMinute < 10 ? startMinute.toString().padStart(2, '0') : startMinute.toString();
        times.push(
          `${String(startHour).padStart(2, '0')}:${minutes}`,
        );
        startMinute += this.hourGap;
        if (startMinute >= 60) {
          startHour += 1;
          startMinute -= 60;
        }
      }
      return times;
    },
    getEventStyle(event) {
      let eventDay = event.day;
      if (event.type === 'event') {
        const eventDate = new Date(event.date * 1000);
        eventDay = eventDate.getUTCDay();
      }
      const startRow = this.times.indexOf(event.time.start) + 2;
      const endRow = this.times.indexOf(event.time.end) + 2;
      return {
        'grid-column': eventDay + 2,
        'grid-row': `${startRow} / ${endRow}`,
        background: this.getEventBackground(event),
      };
    },
    getEventBackground(event) {
      switch (event.type) {
        case 'artwork': return this.localStorage.themeColors.artwork;
        case 'ceramic': return this.localStorage.themeColors.ceramic;
        case 'event': return this.localStorage.themeColors.event;
        case 'lection': return this.localStorage.themeColors.lecture;
        default: return this.localStorage.themeColors.default;
      }
    },
    currentWeek() {
      let currentWeek = this.currentDate.clone();
      if (this.diff < 0) {
        currentWeek = this.currentDate.clone().add(Math.abs(this.diff), 'weeks');
      } else {
        currentWeek = this.currentDate.clone().subtract(Math.abs(this.diff), 'weeks');
      }
      this.currentDate = currentWeek;
      this.diff = 0;
    },
    previousWeek() {
      this.diff -= 1;
      this.currentDate = this.currentDate.clone().subtract(1, 'weeks');
    },
    nextWeek() {
      this.diff += 1;
      this.currentDate = this.currentDate.clone().add(1, 'weeks');
    },
    manageEvents() {
      console.log(this.events);
    },
    thisWeek(event) {
      const eventDate = new Date(event.date * 1000);
      const thisWeek = this.currentDate.clone().week() === eventDate.getWeek();
      const notExcluded = this.isDismissedEvent(event.uid, this.currentDate.clone().week());
      return event.type === 'event' ? thisWeek : !notExcluded;
    },
    isDismissedEvent(uid, week) {
      return this.dismissed.some((obj) => obj.course.uid === uid
        && new Date(obj.date * 1000).getWeek() === week);
    },
    handlePages(event) {
      switch (event.button) {
        case 3: return this.previousWeek();
        case 4: return this.nextWeek();
        default: return '';
      }
    },
    selectEvent(event) {
      this.selectedEvent = event;
      this.selectedEventWeek = event.type !== 'event' ? this.currentDate : null;
    },
    cancelEvent() {
      const event = { ...this.selectedEvent };
      if (this.selectedEvent.type !== 'event') {
        // eslint-disable-next-line
        const eventDate = this.selectedEventWeek.toDate().getDateByWeekDay(this.selectedEvent.day + 1);
        const [startHour, startMinute] = this.selectedEvent.time.start.split(':').map(Number);
        eventDate.setHours(startHour, startMinute, 0);
        event.date = eventDate;
      }
      this.selectedEvent = null;
      this.$emit('dismiss', event);
    },
    deleteEvent() {
      const event = { ...this.selectedEvent };
      this.selectedEvent = null;
      this.$emit('delete', event);
    },
  },
  computed: {
    startOfWeek() {
      this.currentDate.locale('ru');
      return this.currentDate.clone().startOf('isoWeek');
    },
    daysOfWeek() {
      const days = [];
      for (let i = 0; i < 7; i++) {
        days.push(this.startOfWeek.clone().add(i, 'days'));
      }
      return days;
    },
    calendarYear() {
      return this.currentDate.format('YYYY');
    },
    selectedEventTiming() {
      const date = new Date(this.selectedEvent.date * 1000);
      const weekDay = this.initialDays[date.getUTCDay() + 1];
      const weekDate = `${date.getDate()}.${date.getMonth() + 1}`;
      return `${weekDay}, ${weekDate} ${this.selectedEvent.time.start}-${this.selectedEvent.time.end}`;
    },
    accessibleForDelete() {
      const newlyCreatedEvents = Object.keys(this.$parent.localStorage.newEventsList);
      return newlyCreatedEvents.includes(this.selectedEvent.uid);
    },
    // formattedDays() {
    //   this.currentDate.locale('ru');
    //   const weekDays = this.daysOfWeek;
    //   const empty = [''];
    //   const days = empty.concat(weekDays);
    //   console.log(days);
    //   return days;
    // },
  },
  mounted() {
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.calendar{
  overflow: hidden;
  &:has(.calendar_year) &_wrapper{
    margin-top: 0px;
  }
  &_wrapper{
    position: relative;
    margin-top: 30px;
    display: grid;
    grid-template-columns: 1fr repeat(7, 1fr);
    grid-template-rows: auto repeat(22, 1fr);
    border-bottom: 1px solid $black;
    border-right: 1px solid $black;
    grid-gap: 1px;
    user-select: none;
  }
  &_year{
    height: 30px;
    text-align: center;
    font-family: $text-font;
    font-size: 24px;
    border: 1px solid $black;
  }
  &_time{
    grid-column: 1;
    height: 25px;
    border-right: 1px solid $black;
    text-align: center;
    display: flex;
    align-items: center;
    border-bottom: 1px solid transparent;
    font-family: $text-font;
    justify-content: center;
    &:nth-child(2n) {
      border-bottom: 1px solid $black;
    }
  }
  &_day{
    grid-row: 1;
    text-align: center;
    border-bottom: 1px solid $black;
    font-family: $text-font;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    &:nth-child(1n){
      border-right: 1px solid $black;
    }
    &:nth-child(8n + 7){
      border-right-color: transparent !important;
    }
    &-actions{
      display: flex;
      align-items: center;
    }
    &-title{}
    .current_week{
      cursor: pointer;
    }
    &.empty{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
  }
  &_event{
    padding: 5px;
    border-radius: 8px;
    text-align: center;
    font-family: $text-font;
    color: $black !important;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    mix-blend-mode: exclusion;
    cursor: pointer;
    &-name{
      font-weight: bold;
      font-size: 16px;
    }
    &-type{
      font-size: 12px;
    }
  }
  .event_wrapper{
    position: absolute;
    z-index: 3;
    font-family: $text-font;
    right: 10px;
    padding: 15px;
    background: $green;
    color: $white;
    border-radius: 10px;
    top: calc(50% - 100px);
    width: 350px;
    &-close{
      position: absolute;
      left: 2px;
      top: 2px;
      border-radius: 4px;
      height: 25px;
      width: 25px;
    }
    .event_body{
      &-header{
        display: flex;
        align-items: center;
        flex-direction: column;
      }
      &-title{
        font-weight: bold;
        font-size: 18px;
        text-align: center;
      }
      &-teacher{
        display: flex;
        align-items: center;
        padding: 0 15px;
        .m-icon{
          margin-right: 10px;
          cursor: default;
        }
      }
      &-clients{
        padding: 0 15px;
      }
      &-add_client{
        margin: 20px 0 30px 0;
        .add_client-form{
          width: 100%;
          display: flex;
          align-items: center;
          .m-icon{
            margin-left: 10px;
          }
          .input_dropdown{
            margin-top: 0;
            width: 100%;
          }
        }
      }
      &-comment
      ,&-description{
        max-width: 300px;
      }
      &-actions{
        .btn_submit{
          box-shadow: 1px 1px 10px rgba($color: $white, $alpha: .3)
        }
        .delete{
          color: #FE5F5F;
        }
      }
      border-radius: inherit;
      height: 100%;
    }
  }
}
.appear-right-enter-active{
  animation: slide-left .6s ease-in-out;
}
.appear-right-leave-active{
  animation: slide-left .6s ease-in-out reverse;
}

@keyframes slide-left {
  0%{ transform: translateX(100%); }
  100% { transform: translateX(0%); }
}
</style>
