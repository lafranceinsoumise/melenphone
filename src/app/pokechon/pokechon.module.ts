import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CodexComponent } from './views/codex/codex.component';
import { WelcomeComponent } from './views/welcome/welcome.component';

const routes: Routes = [
    { path: '', component: CodexComponent }
];

@NgModule({
    exports: [],
    imports: [
        RouterModule.forChild(routes)
    ],
    declarations: [CodexComponent, WelcomeComponent],
    providers: [],
    entryComponents: []
})
export class PokechonModule {}
