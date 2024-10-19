class Storage {
  newEventsList = {};

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

  timeNow() {
    this.msg = null;
    return new Date() / 1000;
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
  }
}

export default Storage;
