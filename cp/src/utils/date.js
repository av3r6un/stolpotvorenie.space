// import moment from 'moment';

/* eslint-disable */
Date.prototype.getWeek = function () {
  const date = new Date(this.getTime());
  date.setHours(0, 0, 0, 0);
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  const week1 = new Date(date.getFullYear(), 0, 4);
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
}

Date.prototype.getDateByWeekDay = function (weekdayIndex) {
  const date = new Date(this.getTime());
  const currentDay = date.getDay();
  const adjusted = (currentDay === 0 ? 7 : currentDay);
  const dayDiff = weekdayIndex - adjusted;
  date.setDate(date.getDate() + dayDiff);
  return date;
}

Date.prototype.shortDate = function () {
  const date = new Date(this.getTime());
  const dt = date.getDate().toString().padStart(2, '0');
  const month = `${date.getMonth() + 1}`.padStart(2, '0');
  return `${dt}.${month}`;
}

Date.prototype.withinPastDay = function() {
  const date = new Date(this.getTime());
  const now = new Date();
  const diff = (now - date) / (24 * 3600 * 1000); 
  return diff <= 1;
}
