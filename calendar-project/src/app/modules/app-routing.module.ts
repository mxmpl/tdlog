import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CalendarComponent } from '../components/calendar/calendar.component';
import { OuvriersComponent } from '../components/ouvriers/ouvriers.component';
import { ChantiersComponent } from '../components/chantiers/chantiers.component';
import { OuvrierDetailComponent } from '../components/ouvriers-detail/ouvriers-detail.component';
import { ChantierDetailComponent } from '../components/chantiers-detail/chantiers-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/calendar', pathMatch:'full'},
  { path: 'calendar', component: CalendarComponent },
  { path: 'detail/:id', component: OuvrierDetailComponent },
  { path: 'chantiers/detail/:name', component: ChantierDetailComponent },
  { path: 'ouvriers', component: OuvriersComponent },
  { path: 'chantiers', component: ChantiersComponent},
  { path: 'ouvriers-detail', component: OuvrierDetailComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }