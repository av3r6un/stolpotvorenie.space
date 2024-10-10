<template>
  <article class="schedule">
    <div class="base_title changable">Расписание</div>
    <div class="schedule_grid changable">
      <div class="time_slot changable" v-for="time, idx in times" :key="idx">{{ time }}</div>
      <div class="day_header changable" v-for="day, idx in formattedDays" :key="idx">
        <div class="day_header-actions changable" v-if="idx == 0">
          <div class="left_arrow"></div>
          Сегодня
          <div class="right_arrow"></div>
        </div>
        {{ day }}
      </div>
      <div class="event" :class="event.type" v-for="event in events"
        :style="getEventStyle(event)" :key="event.uid"
        @click="selectEvent(event)">
        <span class="event_name">{{ event.group.course.name }}</span>
        <span class="event_type" v-if="event.group.type">({{ event.group.group_type }})</span>
      </div>
    </div>
    <div class="schedule_delimetr">
    </div>
    <div class="schedule_forms">
      <form class="schedule_add-course" @submit.prevent="addNewCourse">
        <div class="schedule_add-title plus-sign changable form_title">Добавить курс</div>
        <input type="text" placeholder="Название" required autocomplete="off"
          v-model="newCourse.name" class="input_wide">
        <dropDown placeholder="Выбрать преподавателя" v-model:selected="newCourse.teacherUid"
          nested :options="teachers" v-if="teachers" nested-param="full_name"
          ref="teacherDropdown"/>
        <textarea class="input_wide" v-model="newCourse.description"
          placeholder="Описание курса"></textarea>
          <!-- <dropDown placeholder="Выбрать день" v-model:selected="newCourse.day" indexed
          :options="days" />
          <dropDown placeholder="Выбратьвремя"v-model:selected="newCourse.time":options="times"/>-->
          <textarea class="input_wide" v-model="newCourse.info"
            placeholder="Дополнительная информация"></textarea>
        <!-- <input type="number" placeholder="Продолжительность (часов)"required autocomplete="off"
          v-model="newCourse.duration" class="input_wide" min="1" max="11"> -->
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
      <form class="schedule_add-event" @submit.prevent="addNewEvent">
        <div class="schedule_add-title plus-sign changable form_title">Добавить событие</div>
        <dropDown placeholder="Выбрать группу" unique :options="groups" v-if="groups"
          v-model:selected="newEvent.groupId" ref="groupDd"/>
        <dropDown placeholder="Выбрать день" indexed :options="days" v-if="days"
          v-model:selected="newEvent.day" ref="dayDd"/>
        <dropDown placeholder="Начало" :options="times" v-if="times"
          v-model:selected="newEvent.timeStart" ref="timesDd"/>
        <dropDown placeholder="Окончание" :options="formattedTimes" v-if="times"
          v-model:selected="newEvent.timeEnd" ref="lastDd" />
        <input type="datetime-local">
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
    <transition name="appear-right">
      <div class="event_wrapper" v-show="selectedEvent" v-if="selectedEvent">
        <div class="event_wrapper-close" @click="closeEventView">
          <div class="fa xmark changable"></div>
        </div>
        <div class="event_body"
          :style="`background: ${getEventBackground(selectedEvent)}`">
          <div class="event_body-title">{{ selectedEvent.group.course.name }}</div>
          <div class="event_body-date">
            {{ this.days[selectedEvent.day] }}
              {{ selectedEvent.timeStart }}-{{ selectedEvent.timeEnd }}
          </div>
          <div class="event_body-teacher">
            {{ extrapolate('teachers', selectedEvent.group.course.teacher_uid).full_name }}
          </div>
          <div class="event_body-group">{{ selectedEvent.group.group_type }}</div>
          <div class="event_body-actions">
            <button class="btn btn_submit" type="button"
              @click="deleteEvent">Удалить</button>
          </div>
        </div>
      </div>
    </transition>
  </article>
</template>
<script>
import dropDown from '../components/dropDown.vue';
import Backend from '../services/backend.service';

export default {
  name: 'ScheduleView',
  components: { dropDown },
  data() {
    return {
      backend: new Backend(),
      days: ['', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
      times: this.generateTimeSlots('11:00', '22:00', '30'),
      events: [],
      newCourse: {
        name: null,
        teacherUid: null,
        description: null,
        info: null,
      },
      newEvent: {
        groupId: null,
        day: null,
        timeStart: null,
        timeEnd: null,
      },
      courses: [],
      groups: [],
      teachers: null,
      selectedEvent: null,
    };
  },
  methods: {
    generateTimeSlots(timeStart, timeEnd, step) {
      const times = [];
      let [startHour, startMinute] = timeStart.split(':').map(Number);
      const [endHour, endMinute] = timeEnd.split(':').map(Number);
      const timeStep = parseInt(step, 10);

      while (startHour < endHour || (startHour === endHour && startMinute <= endMinute)) {
        const minutes = startMinute < 10 ? startMinute.toString().padStart(2, '0') : startMinute.toString();
        times.push(
          `${String(startHour).padStart(2, '0')}:${minutes}`,
        );
        startMinute += timeStep;
        if (startMinute >= 60) {
          startHour += 1;
          startMinute -= 60;
        }
      }
      return times;
    },
    getEventStyle(event) {
      const startRow = this.times.indexOf(event.timeStart) + 2;
      const endRow = this.times.indexOf(event.timeEnd) + 2;
      return {
        'grid-column': event.day + 2,
        'grid-row': `${startRow} / ${endRow}`,
        background: this.getEventBackground(event),
      };
    },
    getEventBackground(event) {
      const type = `${event.group.course.type}-${event.group.type}`;
      switch (type) {
        case 'artwork-children': return 'lightpink';
        case 'ceramic-mixed': return 'lightgreen';
        default: return 'lightgray';
      }
    },
    selectEvent(event) {
      this.selectedEvent = event;
    },
    addNewCourse() {
      this.backend.post('/courses', this.newCourse)
        .then((resp) => {
          const course = this.newCourse;
          course.uid = resp;
          this.courses.push(course);
          this.resetInfo('newCourse');
          this.$refs.teacherDropdown.reset();
        })
        .catch((err) => console.error(err));
    },
    gatherEssentialData() {
      this.backend.get('/schedule/main')
        .then((resp) => {
          this.teachers = resp.teachers;
          this.events = resp.schedule;
          this.days = this.backend.extra.working_days;
          this.times = this.generateTimeSlots(this.backend.extra.time_open, this.backend.extra.time_close, '30');
          this.courses = resp.courses;
          this.groups = resp.groups;
        })
        .catch((err) => console.error(err));
    },
    resetInfo(obj) {
      const localObj = this[obj];
      Object.keys(localObj).forEach((key) => {
        localObj[key] = null;
      });
    },
    addNewEvent() {
      this.backend.post('/schedule', this.newEvent)
        .then((resp) => {
          this.events.push(resp);
          this.resetInfo('newEvent');
          this.$refs.groupDd.reset();
          this.$refs.dayDd.reset();
          this.$refs.timesDd.reset();
          this.$refs.lastDd.reset();
        })
        .catch((err) => console.log(err));
    },
    extrapolate(obj, value) {
      return this[obj].filter((key) => key.uid === value)[0];
    },
    closeEventView() {
      this.selectedEvent = null;
    },
    deleteEvent() {
      console.log('I wiil be deleted!');
    },
  },
  computed: {
    formattedDays() {
      const weekDays = this.days;
      const empty = [''];
      const days = empty.concat(weekDays);
      return days;
    },
    formattedTimes() {
      const selected = this.times.indexOf(this.newEvent.timeStart) + 1;
      const endList = this.times.length;
      return selected ? this.times.slice(selected, endList) : this.times;
    },
  },
  mounted() {
    this.gatherEssentialData();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.schedule{
  overflow: hidden;
  &_forms{
    display: flex;
    justify-content: space-around;
  }
  &_add-course,
  &_add-event{
    max-width: 410px;
    min-width: 380px;
  }
  &_add-course{
    .input_dropdown{
      margin-bottom: 10px;
    }
  }
  &_delimetr{
    margin: 30px 0;
  }
  &_grid{
    margin: 20px;
    display: grid;
    grid-template-columns: 1fr repeat(7, 1fr);
    grid-template-rows: auto repeat(22, 1fr);
    border-bottom: 1px solid $black;
    border-right: 1px solid $black;
    grid-gap: 0px;
    user-select: none;
    .time_slot{
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
    .day_header{
      grid-row: 1;
      text-align: center;
      border-bottom: 1px solid $black;
      font-family: $text-font;
      height: 25px;
      display: flex;
      align-items: center;
      justify-content: center;
      &:nth-child(1n){
        border-right: 1px solid $black;
      }
      &:nth-child(10n + 11){
        border-right-color: transparent;
      }
      &-actions{
        display: flex;
        align-items: center;
      }
    }
    .event{
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
      &_name{
        font-weight: bold;
        font-size: 16px;
      }
      &_type{
        font-size: 12px;
      }
    }
  }
  .event_wrapper{
    position: absolute;
    font-family: $text-font;
    right: 10px;
    top: calc(50% - 200px);
    width: 200px;
    height: 400px;
    border-radius: 10px;
    &-close{
      position: absolute;
      left: 2px;
      top: 2px;
      border-radius: 4px;
      height: 25px;
      width: 25px;
    }
    .event_body{
      &-title{
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        margin-bottom: 5px;
      }
      border-radius: inherit;
      padding: 24px 12px;
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
