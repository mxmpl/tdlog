import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon'; 
import { MatSidenavModule } from '@angular/material/sidenav';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatListModule } from '@angular/material/list'

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatSidenavModule,
	MatToolbarModule,
	MatIconModule,
	BrowserAnimationsModule,
	MatListModule
  ],
  exports: [
  	MatSidenavModule,
	MatToolbarModule,
	MatIconModule,
	BrowserAnimationsModule,
	MatListModule
  ],
})
export class MaterialModule { }
