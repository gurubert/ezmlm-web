<?cs if:Data.List.Features.Crypto ?>
<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- Gnupg: send plaintext if no key is available -->
<?cs call:checkbox("gnupg_plain_without_key") ?>
<?cs /if ?>

