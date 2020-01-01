import { Component, OnInit } from '@angular/core';
import dayGridView from '@fullcalendar/daygrid';
import { CalendarService } from '../../services/calendar.service';

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css']
})

export class CalendarComponent implements OnInit {
  calendarEvents:any[] = [];
  calendarPlugins = [dayGridView];
  constructor(private svc:CalendarService){}
  ngOnInit(){
    this.svc.getData().subscribe
      (
        (data) => 
        {
          this.calendarEvents = data;
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }
      )
  }

}
