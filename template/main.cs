<!-- $Id$ -->

<?cs include:TemplateDir + '/macros.cs' ?>
<?cs include:TemplateDir + '/header.cs' ?>

<!-- this ezmlm-web template follows: <?cs var:Data.Action ?> -->

<?cs include:TemplateDir + '/nav.cs' ?>
<div id="main_content">
	<?cs if:Data.List.Name ?><div id="info_title"><?cs var:Data.List.Name ?> - <?cs
		var:Data.List.Address ?></div><?cs /if ?>
	<?cs if:Data.Error ?>
		<?cs call:error(Data.Error) ?>
	<?cs else ?>
		<?cs if:Data.Warning ?><?cs call:warning(Data.Warning) ?><?cs /if ?>
		<?cs if:Data.Success ?><?cs call:success(Data.Success) ?><?cs /if ?>
		<?cs include:TemplateDir + '/' + Data.Action + '.cs' ?>
	<?cs /if ?>
</div> <!-- end of main_content -->

<?cs include:TemplateDir + '/footer.cs' ?>

