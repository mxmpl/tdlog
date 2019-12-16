import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ChantiersComponent } from './chantiers/chantiers.component';

const routes: Routes = [
  { path: 'chantiers', component: ChantiersComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }