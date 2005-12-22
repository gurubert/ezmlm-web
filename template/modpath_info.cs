<!-- posting moderation -->
<?cs if:Data.List.PostModPath ?>
    <div class="warning">
	    <?cs var:html_escape(Lang.Misc.PostModPathWarn) ?> (<?cs var:Data.List.PostModPath ?>).<br/><?cs var:html_escape(Lang.Misc.SuggestDefaultPath) ?>
    </div>
<?cs /if ?>

<!-- subscription moderation -->
<?cs if:Data.List.SubModPath ?>
    <div class="warning">
	    <?cs var:html_escape(Lang.Misc.SubModPathWarn) ?> (<?cs var:Data.List.SubModPath ?>).<br/><?cs var:html_escape(Lang.Misc.SuggestDefaultPath) ?>
    </div>
<?cs /if ?>

<!-- remote administration -->
<?cs if:Data.List.RemoteAdminPath ?>
    <div class="warning">
	    <?cs var:html_escape(Lang.Misc.RemoteAdminPathWarn) ?> (<?cs var:Data.List.RemoteAdminPath ?>).<br/><?cs var:html_escape(Lang.Misc.SuggestDefaultPath) ?>
    </div>
<?cs /if ?>
