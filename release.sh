#!/bin/bash
set -e

# Получаем текущую версию из manifest.json
CUR_VERSION=$(jq -r .version custom_components/ha_integration_mobile_extra/manifest.json)
IFS='.' read -r MAJOR MINOR PATCH <<< "$CUR_VERSION"
NEW_PATCH=$((PATCH+1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
TAG="v$NEW_VERSION"

# Обновляем версию в manifest.json
jq ".version = \"$NEW_VERSION\"" custom_components/ha_integration_mobile_extra/manifest.json > tmp_manifest.json && mv tmp_manifest.json custom_components/ha_integration_mobile_extra/manifest.json

git add custom_components/ha_integration_mobile_extra/manifest.json
git commit -m "release: v$NEW_VERSION"
git push

# Проверяем, есть ли уже такой тег
if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "Тег $TAG уже существует."
  exit 1
fi

# Получаем предыдущий тег (если есть)
PREV_TAG=$(git tag --sort=-creatordate | head -n1)
if [ "$PREV_TAG" = "$TAG" ]; then
  PREV_TAG=$(git tag --sort=-creatordate | head -n2 | tail -n1)
fi

# Генерируем changelog
if [ -z "$PREV_TAG" ]; then
  CHANGELOG=$(git log --pretty=format:'* %s (%an)' )
else
  CHANGELOG=$(git log "$PREV_TAG"..HEAD --pretty=format:'* %s (%an)')
fi

# Создаём тег
 git tag "$TAG"
 git push origin "$TAG"

# Публикуем релиз на GitHub через gh
if [ -z "$CHANGELOG" ]; then
  CHANGELOG="Initial release."
fi

gh release create "$TAG" --title "$TAG" --notes "$CHANGELOG"

echo "Релиз $TAG опубликован!" 