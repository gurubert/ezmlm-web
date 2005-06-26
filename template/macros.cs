<?cs def:help_icon(helpname) ?><?cs
    each:item = Lang.Helper ?><?cs 
	if:(name(item) == helpname)
	    ?>&nbsp<img src="<?cs var:HelpIconURL ?>" title="<?cs var:item ?>"/><?cs
	/if ?><?cs
    /each ?>
<?cs /def ?>

<?cs def:generic_icon(helptext)
	?>&nbsp<img src="<?cs var:HelpIconURL ?>" title="<?cs var:helptext ?>"/>
<?cs /def ?>
