import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CodexComponent } from './views/codex/codex.component';

const routes: Routes = [
    { path: '', component: CodexComponent }
];

@NgModule({
    exports: [],
    imports: [
        RouterModule.forChild(routes)
    ],
    declarations: [CodexComponent],
    providers: [],
    entryComponents: []
})
export class PokechonModule {}
