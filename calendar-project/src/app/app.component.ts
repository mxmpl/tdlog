import { Component, OnInit } from '@angular/core';
import dayGridView from '@fullcalendar/daygrid';
import { CalendarService } from './calendar.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = 'calendar-project';
  calendarEvents:any[] = [];
  calendarPlugins = [dayGridView];
  constructor(private svc:CalendarService){}
  ngOnInit(){
  	this.svc.getData().subscribe(data=> this.calendarEvents=data);
  }
}
