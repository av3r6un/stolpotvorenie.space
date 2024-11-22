<template>
  <article class="schedule">
    <div class="base_title changable">Расписание</div>
    <Cal :events="events" @dismiss="dismissCourse" :dismissed="dismissed"
      @delete="deleteEvent"/>
    <div class="schedule_delimetr">
    </div>
    <div class="schedule_forms">
      <form class="schedule_add-course" @submit.prevent="addNewCourse">
        <div class="schedule_add-title plus-sign changable form_title">Добавить курс</div>
        <input type="text" placeholder="Название" required autocomplete="off"
          v-model="newCourse.name" class="input_wide">
        <dropDown placeholder="Выбрать преподавателя" v-model:selected="newCourse.executiveUid"
          nested :options="admins" v-if="admins" nested-param="fullName"
          ref="teacherDropdown"/>
        <textarea class="input_wide" v-model="newCourse.description"
          placeholder="Описание курса"></textarea>
        <dropDown placeholder="Выбрать день" v-model:selected="newCourse.day" indexed
          :options="days" ref="cDayDd"/>
        <div class="form_line">
          <dropDown placeholder="Время начала" v-model:selected="newCourse.timeStart"
            :options="times" ref="cTimesDd"/>
          <dropDown placeholder="Время окончания" v-model:selected="newCourse.timeEnd"
            :options="formattedTimes" v-if="times" ref="cTimesendDd"/>
        </div>
        <textarea class="input_wide" v-model="newCourse.info"
          placeholder="Дополнительная информация"></textarea>
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
      <form class="schedule_add-event" @submit.prevent="addNewEvent">
        <div class="schedule_add-title plus-sign changable form_title">Добавить событие</div>
        <input type="text" class="input_wide" placeholder="Название" v-model="newEvent.name"
          required autocomplete="off">
        <dropDown placeholder="Выбрать ответственного" nested :options="admins" v-if="admins"
          v-model:selected="newEvent.executiveUid" ref="executiveDD" nested-param="fullName" />
        <input type="datetime-local" class="input_wide input_date" v-model="newEvent.date">
        <input type="number" min="1" max="11" class="input_wide" placeholder="Продолжительность"
          v-model="newEvent.duration">
        <dropDown placeholder="Возрастное ограничение" v-model:selected="newEvent.age"
          :options="ages" ref="ageDd"/>
        <textarea class="input_wide" v-model="newEvent.comment"
          placeholder="Комментарий"></textarea>
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
  </article>
</template>
<script>
import dropDown from '../components/dropDown.vue';
import Cal from '../components/calendar.vue';
import Backend from '../services/backend.service';

export default {
  name: 'ScheduleView',
  components: { dropDown, Cal },
  data() {
    return {
      backend: new Backend(),
      ages: ['0+', '6+', '12+', '18+'],
      days: null,
      times: null,
      admins: [],
      events: [],
      dismissed: [],
      courseDropdowns: ['teacherDropdown', 'cDayDd', 'cTimesDd', 'cTimesendDd'],
      eventsDropdowns: ['executiveDD', 'ageDd'],
      localStorage: this.$parent.$parent.localStorage,
      newCourse: {
        name: null,
        executiveUid: null,
        description: null,
        info: null,
        day: null,
        timeStart: null,
        timeEnd: null,
      },
      newEvent: {
        name: null,
        executiveUid: null,
        date: null,
        duration: null,
        age: null,
        comment: null,
      },
      courses: [],
      groups: [],
      teachers: null,
      selectedEvent: null,
    };
  },
  methods: {
    selectEvent(event) {
      this.selectedEvent = event;
    },
    addNewCourse() {
      this.backend.post('/courses', this.newCourse)
        .then((resp) => {
          const courseObj = resp;
          this.events.push(courseObj);
          this.resetInfo('newCourse');
          this.courseDropdowns.forEach((name) => {
            this.$refs[name].reset();
          });
          this.localStorage.storeEvent(courseObj.uid);
          console.log(this.localStorage);
        })
        .catch((err) => console.error(err));
    },
    gatherEssentialData() {
      this.backend.get('/schedule/main')
        .then((resp) => {
          this.events = resp.events;
          this.admins = resp.admins;
          this.dismissed = resp.dismissed;
          this.days = this.backend.extra.working_days;
          this.times = this.generateTimeSlots(
            this.backend.extra.time_open,
            this.backend.extra.time_close,
            '30',
          );
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
      this.backend.post('/events', this.newEvent)
        .then((resp) => {
          this.events.push(resp);
          this.resetInfo('newEvent');
          this.eventsDropdowns.forEach((name) => {
            this.$refs[name].reset();
          });
          this.localStorage.storeEvent(resp.uid);
        })
        .catch((err) => console.log(err));
    },
    extrapolate(obj, value) {
      return this[obj].filter((key) => key.uid === value)[0];
    },
    deleteEvent(event) {
      const url = `/${event.type}/${event.uid}`;
      this.backend.delete(url)
        .then((resp) => {
        // delete from table;
          console.log(resp);
        })
        .catch((err) => console.error(err));
    },
    generateTimeSlots(hourStart, hourEnd, hourGap) {
      const times = [];
      let [startHour, startMinute] = hourStart.split(':').map(Number);
      const [endHour, endMinute] = hourEnd.split(':').map(Number);

      const step = parseInt(hourGap, 10);

      while (startHour < endHour || (startHour === endHour && startMinute <= endMinute)) {
        const minutes = startMinute < 10 ? startMinute.toString().padStart(2, '0') : startMinute.toString();
        times.push(
          `${String(startHour).padStart(2, '0')}:${minutes}`,
        );
        startMinute += step;
        if (startMinute >= 60) {
          startHour += 1;
          startMinute -= 60;
        }
      }
      return times;
    },
    dismissCourse(course) {
      this.backend.put(`/course/${course.uid}`, { date: Math.floor(course.date / 1000) })
        .then((resp) => {
          this.dismissed.push(resp);
        })
        .catch((err) => console.error(err));
    },
  },
  computed: {
    formattedTimes() {
      const selected = this.times.indexOf(this.newCourse.timeStart) + 1;
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
    .form_line{
      display: flex;
      align-items: center;
      justify-content: space-between;
      .input_wide{
        width: 45% !important;
      }
      .input_dropdown{
        margin-bottom: 0;
        margin-top: 0;
        width: 48%;
      }
    }
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
}
</style>
