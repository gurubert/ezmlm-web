<?cs def:help_icon(helpname) ?><?cs
    each:item = Lang.Helper ?><?cs 
	if:(name(item) == helpname)
	    ?>&nbsp;<img src="<?cs var:HelpIconURL ?>" title="<?cs var:item ?>"/><?cs
	/if ?><?cs
    /each ?><?cs
 /def ?>

<?cs def:help_title(helpname) ?><?cs
    each:item = Lang.Helper ?><?cs 
	if:(name(item) == helpname)
	    ?>title="<?cs var:item ?>"<?cs
	/if ?><?cs
    /each ?><?cs
 /def ?>

<?cs def:generic_icon(helptext)
	?>&nbsp<img src="<?cs var:HelpIconURL ?>" title="<?cs var:helptext ?>"/><?cs
 /def ?>

<?cs def:warning(warnname) ?><?cs
    each:item = Lang.WarningMessage ?><?cs 
      if:(name(item) == warnname)
        ?><div class="warning"><?cs var:item ?></div>
	<?cs
      /if ?><?cs
    /each ?><?cs
/def ?>

<?cs def:error(errname) ?><?cs
    each:item = Lang.ErrorMessage ?><?cs 
      if:(name(item) == errname)
        ?><div class="error"><?cs var:item ?></div>
	<?cs
      /if ?><?cs
    /each ?><?cs
/def ?>

<?cs def:success(succname) ?><?cs
    each:item = Lang.SuccessMessage ?><?cs 
      if:(name(item) == succname)
        ?><div class="success"><?cs var:item ?></div>
	<?cs
      /if ?><?cs
    /each ?><?cs
/def ?>

