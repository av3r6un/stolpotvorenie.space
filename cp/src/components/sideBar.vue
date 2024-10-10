<template>
  <nav class="sidebar" :class="!short ? 'long' : ''">
    <div class="sidebar_wrapper">
      <ul class="sidebar_nav">
        <li class="sidebar_item logo" :class="dark ? 'dark' : ''">
          <router-link to="/">
            <logoType :short="short" />
          </router-link>
        </li>
        <li class="sidebar_item" :class="short ? 'short' : ''">
          <router-link to="/clients" class="base_link">
            <mIcon name="users" />
            <span class="sidebar_item-title" v-if="!short">Пользователи</span>
          </router-link>
        </li>
        <li class="sidebar_item" :class="short ? 'short' : ''">
          <router-link to="/groups" class="base_link">
            <mIcon name="user-groups" />
            <span class="sidebar_item-title" v-if="!short">Группы</span>
          </router-link>
        </li>
        <li class="sidebar_item" :class="short ? 'short' : ''">
          <router-link to="/schedule" class="base_link">
            <mIcon name="schedule" />
            <span class="sidebar_item-title" v-if="!short">Расписание</span>
          </router-link>
        </li>
        <li class="sidebar_item" :class="short ? 'short' : ''">
          <router-link to="/attendence" class="base_link">
            <mIcon name="attendence" />
            <span class="sidebar_item-title" v-if="!short">Посещения</span>
          </router-link>
        </li>
        <li class="sidebar_item" :class="short ? 'short' : ''">
          <router-link to="/teachers" class="base_link">
            <mIcon name="teachers" />
            <span class="sidebar_item-title" v-if="!short">Преподаватели</span>
          </router-link>
        </li>
        <li class="sidebar_item" :class="short ? 'short' : ''"
          v-if="$store.getters.isAuth">
          <div class="base_link" @click="$store.dispatch('logout')">
            <mIcon name="logout" />
            <span class="sidebar_item-title" v-if="!short">{{ $store.getters.name }}</span>
          </div>
        </li>
        <li class="sidebar_item" :class="short ? 'short': ''" v-else>
          <router-link to="/login" class="base_link">
            <mIcon name="login" />
            <span class="sidebar_item-title" v-if="!short">Авторизация</span>
          </router-link>
        </li>
      </ul>
      <div class="sidebar_button" @click="toggleSidebar" :class="short ? 'outside' : ''">
        <mIcon :name="arrows" :width="27" :height="24" />
      </div>
      <div class="sidebar_theme" @click="toggleTheme" v-show="!short">
        <mIcon :name="dark ? 'sun' : 'moon'" :width="24" :height="24" />
      </div>
    </div>
  </nav>
</template>
<script>
import logoType from './logoType.vue';
import mIcon from './materialIcon.vue';

export default {
  name: 'sideBar',
  components: { logoType, mIcon },
  data() {
    return {
      short: false,
      currentRoute: null,
      dark: false,
    };
  },
  methods: {
    isActive(event) {
      console.log('event: ', event);
    },
    toggleSidebar() {
      this.short = !this.short;
      this.$emit('sidebar-toggled', !this.short);
    },
    hideSidebar() {
      this.short = true;
      this.$emit('sidebar-toggled', false);
    },
    toggleTheme() {
      this.dark = !this.dark;
      this.$emit('theme', this.dark);
    },
  },
  computed: {
    arrows() {
      return `arrow-${this.short ? 'right' : 'left'}`;
    },
  },
  mounted() {
  },
  deactivated() {
    // document.querySelector('a.base_link').removeEventListener('click', this.shortAnalyze);
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.sidebar{
  width: 75px;
  transition: all .4s ease-in;
  &.long{
    width: 350px;
  }
  position: fixed;
  height: 100%;
  &_nav{
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 0 0 35px 0;
    box-sizing: border-box;
    overflow: hidden;
  }
  &_item {
    font-family: $text-font;
    font-size: 18px;
    color: $white;
    list-style-type: none;
    margin-left: 20px;
    padding: 5px 0 5px 15px;
    margin-bottom: 25px;
    transition: all .4s ease-in;
    &.short{
      margin: 10px;
      padding: 10px;
      border-radius: 8px !important;
      .m-icon{
        margin-right: 0;
      }
    }
    &:hover:not(&:first-child) {
      box-shadow: 1px 1px 10px 1px rgba($color: black, $alpha: .5);
      border-radius: 10px 0 0 10px;
    }
    &:has(> a.active):not(&:first-child) {
      box-shadow: 1px 1px 10px 1px rgba($color: black, $alpha: .5);
      border-radius: 10px 0 0 10px;
    }
    .base_link{
      display: flex;
      align-items: center;
    }
    &.logo{
      margin-left: 0;
      margin-bottom: 0;
      padding: 25px 0;
      background: white;
      justify-content: center;
      border-radius: 0 !important;
      transition: background .4s ease-in;
      &.dark{
        background: $bg-color;
      }
    }
    &:nth-child(2) {
      margin-top: 70px;
    }
    &:last-child{
      margin-top: auto;
      margin-bottom: 0;
    }
    &:last-child,
    &.logo{
      box-shadow: none;
    }
    .m-icon{
      margin-right: 32px;
    }
  }
  &_wrapper{
    height: 100%;
    background: $green;
    position: relative;
  }
  &_theme{
    position: absolute;
    top: 90px;
    right: 15px;
  }
  &_button{
    position: absolute;
    top: 50%;
    right: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 30px;
    width: 30px;
    border-radius: 7px;
    transition: right .4s ease-in;
    z-index: 10;
    &:hover{
      box-shadow: inset 1px 1px 10px rgba($color: $black, $alpha: .3);
    }
    &.outside{
      background: $green;
      right: -35px;
    }
  }
}
</style>
