class Storage {
  newEventsList = {};

  themeColors = {
    dark: false,
    artwork: '#ff9501', // '#F6C3AE', '#CAFDD8',
    ceramic: '#83afee', // '#9AB2D4', '#61BE91',
    event: '#e99ddd', // '#AAD59E', '#B16959',
    lection: '#4c5f43', // '#F0743E', // '#FCCAFD',
    default: 'lightgrey',
  };

  constructor() {
    this.loadStorage();
  }

  loadStorage() {
    const lS = localStorage.getItem('_events');
    const events = lS ? JSON.parse(lS) : null;
    if (events) {
      const validEvents = this.validateEvents(events);
      this.newEventsList = { ...validEvents };
    }
    const bS = localStorage.getItem('_settings');
    if (!bS) {
      localStorage.setItem('_settings', JSON.stringify(this.themeColors));
    } else {
      this.themeColors = { ...JSON.parse(bS) };
    }
  }

  validateEvents(eventList) {
    const cleanEvents = {};
    Object.keys(eventList).forEach((key) => {
      if (!this.olderThen(eventList[key].dateAdded, 24)) {
        cleanEvents[key] = eventList[key];
      }
    });
    return cleanEvents;
  }

  storeEvent(uid) {
    this.newEventsList[uid] = this.timeNow();
    this.save();
  }

  dustEvent(uid) {
    delete this.newEventsList[uid];
    this.save();
  }

  gatherEvent(uid) {
    return this.newEventsList[uid];
  }

  timeNow() {
    this.msg = null;
    return new Date() / 1000;
  }

  changeColorSettings(name, color) {
    this.themeColors[name] = color;
    localStorage.setItem('_settings', JSON.stringify(this.themeColors));
  }

  olderThen(datetime, hours) {
    const dt = new Date(datetime * 1000);
    const now = this.timeNow();
    const diffMs = Math.abs(now - dt);
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    return diffHours > hours;
  }

  save() {
    localStorage.setItem('_events', JSON.stringify(this.newEventsList));
    localStorage.setItem('_settings', JSON.stringify(this.themeColors));
  }
}

export default Storage;
