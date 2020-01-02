import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FullCalendarModule } from '@fullcalendar/angular';
import { HttpClientModule } from '@angular/common/http';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AppComponent } from './app.component';
import { CalendarComponent } from './components/calendar/calendar.component';
import { HeaderComponent } from './components/header/header.component';
import { OuvriersComponent } from './components/ouvriers/ouvriers.component';
import { LayoutComponent } from './components/layout/layout.component'
import { ChantiersComponent } from './components/chantiers/chantiers.component';
import { SidenavListComponent } from './components/sidenav-list/sidenav-list.component'

import { CalendarService } from './services/calendar.service';
import { AppRoutingModule } from './app-routing.module';
import { MaterialModule } from './modules/material/material.module';

@NgModule({
  declarations: [
    AppComponent,
    CalendarComponent,
    HeaderComponent,
    OuvriersComponent,
    LayoutComponent,
    SidenavListComponent,
    ChantiersComponent
  ],
  imports: [
    BrowserModule,
    FullCalendarModule,
    AppRoutingModule,
    HttpClientModule,
    MaterialModule,
    FlexLayoutModule
  ],
  providers: [CalendarService],
  bootstrap: [AppComponent]
})
export class AppModule { }
