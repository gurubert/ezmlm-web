<!-- $opts -->
<p>
<!-- TODO: das sollte so etwas, wie eine Tabelle werden -->
	<?cs each:item = Data.List.Options ?>
	    <div class="checkbox"><input type="checkbox"
	      name="<?cs var:item.name ?>" value="<?cs var:item.name ?>"
	      <?cs if:item.state ?> checked="checked"<?cs /if ?>>
	      <?cs var:item.short ?><?cs call:generic_icon(item.long) ?></div>
	<?cs /each ?>
</p>

<p>
	<?cs each:item = Data.List.Settings ?>
	    <div class="checkbox"><input type="checkbox" name="<?cs var:item.name ?>"
	      value="<?cs var:item.name ?>"<?cs if:item.state ?> checked="checked"<?cs /if ?>>
	      <?cs var:item.short ?>
	      <span class="formfield"><input type="text" name="<?cs var:item.name ?>-value"
	      value="<?cs var:item.value ?>" size="30">
	      <?cs call:generic_icon(item.long) ?></div>
	      <!-- TODO: die indirekte Namensangabe des textfield is unsauber - sollte nicht
	        mit dem Code vermischt sein -->
	<?cs /each ?>
</p>
