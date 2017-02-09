import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CodexComponent } from './codex/codex.component';

const routes: Routes = [
    { path: '/coucou' }
];

@NgModule({
    exports: [],
    imports: [
        RouterModule.forRoot(routes)
    ],
    declarations: [CodexComponent],
    providers: [],
    entryComponents: []
})
export class PokechonModule {}