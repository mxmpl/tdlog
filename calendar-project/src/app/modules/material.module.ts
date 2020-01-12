import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon'; 
import { MatSidenavModule } from '@angular/material/sidenav';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatListModule } from '@angular/material/list'
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatRadioModule} from '@angular/material/radio';
import {MatExpansionModule} from '@angular/material/expansion'; 
import {MatDividerModule} from '@angular/material/divider'; 
import {MatFormFieldModule} from '@angular/material/form-field'; 
import {MatInputModule} from '@angular/material/input'; 
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card'; 
import {MatSlideToggleModule} from '@angular/material/slide-toggle'; 

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatSidenavModule,
	MatToolbarModule,
	MatIconModule,
	BrowserAnimationsModule,
	MatListModule,
	MatCheckboxModule,
	MatRadioModule,
	MatExpansionModule,
	MatDividerModule,
	MatFormFieldModule,
	MatInputModule,
	MatButtonModule,
	MatCardModule,
	MatSlideToggleModule
  ],
  exports: [
  	MatSidenavModule,
	MatToolbarModule,
	MatIconModule,
	BrowserAnimationsModule,
	MatListModule,
	MatCheckboxModule,
	MatRadioModule,
	MatExpansionModule,
	MatDividerModule,
	MatFormFieldModule,
	MatButtonModule,
	MatInputModule,
	MatCardModule,
	MatSlideToggleModule
  ],
})
export class MaterialModule { }
