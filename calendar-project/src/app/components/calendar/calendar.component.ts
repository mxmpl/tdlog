import { Component, ViewChild } from '@angular/core';
import { FullCalendarComponent } from '@fullcalendar/angular';
import { EventInput } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGrigPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction'; // for dateClick

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css']
})

export class CalendarComponent {

  calendarPlugins = [dayGridPlugin, timeGrigPlugin, interactionPlugin];
  calendarWeekends = true;
  calendarEvents = {
  	url: 'http://127.0.0.1:5000/listeChantiers/',
	color: 'yellow',
	textColor: 'black'
  };

  toggleWeekends() {
    this.calendarWeekends = !this.calendarWeekends;
  }

  handleDateClick(arg) {
    if (confirm('Would you like to add an event to ' + arg.dateStr + ' ?')) {
      console.log('ok')
    }
  }

  handleEventDragStart(timeSheetEntry, jsEvent, ui, activeView) {
   console.log('event drag start');
  }
  handleEventDragStop(timeSheetEntry, jsEvent, ui, activeView) {
   console.log('event drag end');
  }

}