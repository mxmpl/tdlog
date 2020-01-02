import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon'; 
import { MatSidenavModule } from '@angular/material/sidenav';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatSidenavModule,
	MatToolbarModule,
	MatIconModule,
	BrowserAnimationsModule
  ],
  exports: [
  	MatSidenavModule,
	MatToolbarModule,
	MatIconModule,
	BrowserAnimationsModule
  ],
})
export class MaterialModule { }
