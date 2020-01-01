import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CalendarService } from './services/calendar.service';
import { FullCalendarModule } from '@fullcalendar/angular';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    FullCalendarModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [CalendarService],
  bootstrap: [AppComponent]
})
export class AppModule { }
