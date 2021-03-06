import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
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

import { AppRoutingModule } from './modules/app-routing.module';
import { MaterialModule } from './modules/material.module';
import { OuvrierDetailComponent } from './components/ouvriers-detail/ouvriers-detail.component';
import { MessagesComponent } from './components/messages/messages.component';
import { ChantierDetailComponent } from './components/chantiers-detail/chantiers-detail.component';

import {MAT_DATE_LOCALE} from '@angular/material';

@NgModule({
  declarations: [
    AppComponent,
    CalendarComponent,
    HeaderComponent,
    OuvriersComponent,
    LayoutComponent,
    SidenavListComponent,
    ChantiersComponent,
    OuvrierDetailComponent,
    MessagesComponent,
    ChantierDetailComponent
  ],
  imports: [
    BrowserModule,
    FullCalendarModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    MaterialModule,
    FlexLayoutModule
  ],
  providers: [{provide: MAT_DATE_LOCALE, useValue:'fr-FR'}],
  bootstrap: [AppComponent]
})
export class AppModule { }
