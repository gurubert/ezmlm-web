<!-- posting moderation -->
<?cs if:Data.List.PostModPath ?>
    <div class="warning">
	    <?cs var:Lang.Misc.PostModPathWarn ?> (<?cs var:Data.List.PostModPath ?>). <?cs var:Lang.Misc.SuggestDefaultPath ?>
    </div>
<?cs /if ?>

<!-- subscription moderation -->
<?cs if:Data.List.SubModPath ?>
    <div class="warning">
	    <?cs var:Lang.Misc.SubModPathWarn ?> (<?cs var:Data.List.SubModPath ?>). <?cs var:Lang.Misc.SuggestDefaultPath ?>
    </div>
<?cs /if ?>

<!-- remote administration -->
<?cs if:Data.List.RemoteAdminPath ?>
    <div class="warning">
	    <?cs var:Lang.Misc.RemoteAdminPathWarn ?> (<?cs var:Data.List.RemoteAdminPath ?>). <?cs var:Lang.Misc.SuggestDefaultPath ?>
    </div>
<?cs /if ?>
