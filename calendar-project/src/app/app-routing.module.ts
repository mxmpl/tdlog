import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CalendarComponent } from './components/calendar/calendar.component';
import { OuvriersComponent } from './components/ouvriers/ouvriers.component';

const routes: Routes = [
  { path: 'calendar', component: CalendarComponent },
  { path: 'ouvriers', component: OuvriersComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }